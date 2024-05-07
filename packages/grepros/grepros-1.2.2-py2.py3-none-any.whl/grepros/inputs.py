# -*- coding: utf-8 -*-
"""
Input sources for ROS messages.

------------------------------------------------------------------------------
This file is part of grepros - grep for ROS bag files and live topics.
Released under the BSD License.

@author      Erki Suurjaak
@created     23.10.2021
@modified    20.04.2024
------------------------------------------------------------------------------
"""
## @namespace grepros.inputs
from __future__ import print_function
import collections
import datetime
import functools
import itertools
import os
try: import queue  # Py3
except ImportError: import Queue as queue  # Py2
import re
import threading
import time
import traceback

import six

from . import api
from . import common
from . common import ArgumentUtil, ConsolePrinter, ensure_namespace, drop_zeros


class Source(object):
    """Message producer base class."""

    ## Returned from read() as (topic name, ROS message, ROS timestamp object).
    class SourceMessage(api.Bag.BagMessage): pass

    ## Template for message metainfo line
    MESSAGE_META_TEMPLATE = "{topic} #{index} ({type}  {dt}  {stamp})"

    ## Constructor argument defaults
    DEFAULT_ARGS = dict(START_TIME=None, END_TIME=None, START_INDEX=None, END_INDEX=None,
                        UNIQUE=False, SELECT_FIELD=(), NOSELECT_FIELD=(),
                        NTH_MESSAGE=1, NTH_INTERVAL=0, PROGRESS=False)

    def __init__(self, args=None, **kwargs):
        """
        @param   args                   arguments as namespace or dictionary, case-insensitive
        @param   args.start_time        earliest timestamp of messages to read
        @param   args.end_time          latest timestamp of messages to read
        @param   args.unique            emit messages that are unique in topic
        @param   args.start_index       message index within topic to start from
        @param   args.end_index         message index within topic to stop at
        @param   args.select_field      message fields to use for uniqueness if not all
        @param   args.noselect_field    message fields to skip for uniqueness
        @param   args.nth_message       read every Nth message in topic, starting from first
        @param   args.nth_interval      minimum time interval between messages in topic,
                                        as seconds or ROS duration
        @param   args.progress          whether to print progress bar
        @param   kwargs                 any and all arguments as keyword overrides, case-insensitive
        """
        # {key: [(() if any field else ('nested', 'path') or re.Pattern, re.Pattern), ]}
        self._patterns = {}
        # {topic: ["pkg/MsgType", ]} searched in current source
        self._topics = collections.defaultdict(list)
        self._counts = collections.Counter()  # {(topic, typename, typehash): count processed}
        # {(topic, typename, typehash): (message hash over all fields used in matching)}
        self._hashes = collections.defaultdict(set)
        self._processables  = {}  # {(topic, typename, typehash): (index, stamp) of last processable}
        self._start_indexes = {}  # {(topic, typename, typehash): index to start producing from}
        self._end_indexes   = {}  # {(topic, typename, typehash): index to stop producing at}
        self._bar_args      = {}  # Progress bar options
        self._status = None  # Processable/match status of last produced message

        self.args = ensure_namespace(args, Source.DEFAULT_ARGS, **kwargs)
        ## outputs.Sink instance bound to this source
        self.sink = None
        ## All topics in source, as {(topic, typenane, typehash): total message count or None}
        self.topics = {}
        ## ProgressBar instance, if any
        self.bar = None
        ## Result of validate()
        self.valid = None
        ## Apply all filter arguments when reading, not only topic and type
        self.preprocess = True

        self._parse_patterns()

    def __iter__(self):
        """Yields messages from source, as (topic, msg, ROS time)."""
        return self.read()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Context manager exit, closes source."""
        self.close()

    def read(self):
        """Yields messages from source, as (topic, msg, ROS time)."""

    def bind(self, sink):
        """Attaches sink to source"""
        self.sink = sink

    def configure(self, args=None, **kwargs):
        """
        Updates source configuration.

        @param   args    arguments as namespace or dictionary, case-insensitive
        @param   kwargs  any and all arguments as keyword overrides, case-insensitive
        """
        self.args = ensure_namespace(args, vars(self.args), **kwargs)
        self.valid = None

    def validate(self):
        """Returns whether arguments are valid and source prerequisites are met."""
        if self.valid is not None: return self.valid
        try: self.args, self.valid = ArgumentUtil.validate(self.args), True
        except Exception: self.valid = False
        return self.valid

    def close(self):
        """Shuts down input, closing any files or connections."""
        self.topics.clear()
        self._topics.clear()
        self._counts.clear()
        self._hashes.clear()
        self._processables.clear()
        self._status = None
        if self.bar:
            self.bar.pulse_pos = None
            self.bar.update(flush=True).stop()
            self.bar = None

    def close_batch(self):
        """Shuts down input batch if any (like bagfile), else all input."""
        self.close()

    def format_meta(self):
        """Returns source metainfo string."""
        return ""

    def format_message_meta(self, topic, msg, stamp, index=None):
        """Returns message metainfo string."""
        meta = self.get_message_meta(topic, msg, stamp, index)
        meta = {k: "" if v is None else v for k, v in meta.items()}
        return self.MESSAGE_META_TEMPLATE.format(**meta)

    def get_batch(self):
        """Returns source batch identifier if any (like bagfile name if BagSource)."""

    def get_meta(self):
        """Returns source metainfo data dict."""
        return {}

    def get_message_meta(self, topic, msg, stamp, index=None):
        """Returns message metainfo data dict."""
        with api.TypeMeta.make(msg, topic) as m:
            return dict(topic=topic, type=m.typename, stamp=drop_zeros(api.to_sec(stamp)),
                        index=index, dt=drop_zeros(common.format_stamp(api.to_sec(stamp)), " "),
                        hash=m.typehash, schema=m.definition)

    def get_message_class(self, typename, typehash=None):
        """Returns message type class."""
        return api.get_message_class(typename)

    def get_message_definition(self, msg_or_type):
        """Returns ROS message type definition full text, including subtype definitions."""
        return api.get_message_definition(msg_or_type)

    def get_message_type_hash(self, msg_or_type):
        """Returns ROS message type MD5 hash."""
        return api.get_message_type_hash(msg_or_type)

    def is_processable(self, topic, msg, stamp, index=None):
        """Returns whether message passes source filters; registers status."""
        if self.args.START_TIME and stamp < self.args.START_TIME:
            return False
        if self.args.END_TIME and stamp > self.args.END_TIME:
            return False
        if self.args.START_INDEX or self.args.END_INDEX \
        or self.args.NTH_MESSAGE or self.args.UNIQUE:
            topickey = api.TypeMeta.make(msg, topic).topickey
        if self.args.START_INDEX and index is not None:
            if max(0, self._start_indexes.get(topickey, self.args.START_INDEX)) > index:
                return False
        if self.args.END_INDEX and index is not None:
            if self._end_indexes.get(topickey, self.args.END_INDEX) < index:
                return False
        if self.args.NTH_MESSAGE > 1 or self.args.NTH_INTERVAL > 0:
            last_accepted = self._processables.get(topickey)
        if self.args.NTH_MESSAGE > 1 and last_accepted and index is not None:
            shift = self.args.START_INDEX if (self.args.START_INDEX or 0) > 1 else 1
            if (index - shift) % self.args.NTH_MESSAGE:
                return False
        if self.args.NTH_INTERVAL > 0 and last_accepted and stamp is not None:
            if api.to_sec(stamp - last_accepted[1]) < self.args.NTH_INTERVAL:
                return False
        if self.args.UNIQUE:
            include, exclude = self._patterns["select"], self._patterns["noselect"]
            msghash = api.make_message_hash(msg, include, exclude)
            if msghash in self._hashes[topickey]:
                return False
            self._hashes[topickey].add(msghash)
        self._status = True
        return True

    def notify(self, status):
        """Reports match status of last produced message."""
        self._status = bool(status)
        if self.bar and self._bar_args.get("source_value") is not None:
            self.bar.update(self.bar.value + bool(status))

    def configure_progress(self, **kwargs):
        """Configures progress bar options, updates current bar if any."""
        for k, v in kwargs.items():
            if isinstance(self._bar_args.get(k), dict) and isinstance(v, dict):
                self._bar_args[k].update(v)
            else: self._bar_args[k] = v
        if self.bar:
            bar_attrs = set(k for k in vars(self.bar) if not k.startswith("_"))
            for k, v in self._bar_args.items():
                if k in bar_attrs: setattr(self.bar, k, v)
                else: self.bar.afterargs[k] = v

    def init_progress(self):
        """Initializes progress bar, if any."""
        if self.args.PROGRESS and not self.bar:
            self.bar = common.ProgressBar(**self._bar_args)
            self.bar.start() if self.bar.pulse else self.bar.update(value=0)

    def update_progress(self, count, running=True):
        """Updates progress bar, if any, with source processed count, pauses bar if not running."""
        if self.bar:
            if not running:
                self.bar.pause, self.bar.pulse_pos = True, None
            if self._bar_args.get("source_value") is not None:
                self.bar.afterargs["source_value"] = count
            else: self.bar.update(count)

    def thread_excepthook(self, text, exc):
        """Handles exception, used by background threads."""
        ConsolePrinter.error(text)

    def _parse_patterns(self):
        """Parses pattern arguments into re.Patterns."""
        selects, noselects = self.args.SELECT_FIELD, self.args.NOSELECT_FIELD
        for key, vals in [("select", selects), ("noselect", noselects)]:
            self._patterns[key] = [(tuple(v.split(".")), common.path_to_regex(v)) for v in vals]


class ConditionMixin(object):
    """
    Provides topic conditions evaluation.

    Evaluates a set of Python expressions, with a namespace of:
    - msg:                current message being checked
    - topic:              current topic being read
    - <topic /any/name>   messages in named or wildcarded topic

    <topic ..> gets replaced with an object with the following behavior:
    - len(obj)  -> number of messages processed in topic
    - bool(obj) -> whether there are any messages in topic
    - obj[pos]  -> topic message at position (from latest if negative, first if positive)
    - obj.x     -> attribute x of last message

    All conditions need to evaluate as true for a message to be processable.
    If a condition tries to access attributes of a message not yet present,
    condition evaluates as false.

    If a condition topic matches more than one real topic (by wildcard or by
    different types in one topic), evaluation is done for each set of
    topics separately, condition passing if any set passes.

    Example condition: `<topic */control_enable>.data and <topic */cmd_vel>.linear.x > 0`
                       `and <topic */cmd_vel>.angular.z < 0.02`.
    """

    TOPIC_RGX = re.compile(r"<topic\s+([^\s><]+)\s*>")  # "<topic /some/thing>"

    ## Constructor argument defaults
    DEFAULT_ARGS = dict(CONDITION=())

    class NoMessageException(Exception): pass


    class Topic(object):
        """
        Object for <topic x> replacements in condition expressions.

        - len(topic)        -> number of messages processed in topic
        - bool(topic)       -> whether there are any messages in topic
        - topic[x]          -> history at -1 -2 for last and but one, or 0 1 for first and second
        - topic.x           -> attribute x of last message
        - value in topic    -> whether any field of last message contains value
        - value in topic[x] -> whether any field of topic history at position contains value
        """

        def __init__(self, count, firsts, lasts):
            self._count  = count
            self._firsts = firsts
            self._lasts  = lasts

        def __bool__(self):    return bool(self._count)
        def __nonzero__(self): return bool(self._count)
        def __len__(self):     return self._count

        def __contains__(self, item):
            """Returns whether value exists in last message, or raises NoMessageException."""
            if not self._lasts: raise ConditionMixin.NoMessageException()
            return item in ConditionMixin.Message(self._lasts[-1])

        def __getitem__(self, key):
            """Returns message from history at key, or Empty() if no such message."""
            try: return ConditionMixin.Message((self._lasts if key < 0 else self._firsts)[key])
            except IndexError: return ConditionMixin.Empty()

        def __getattr__(self, name):
            """Returns attribute value of last message, or raises NoMessageException."""
            if not self._lasts: raise ConditionMixin.NoMessageException()
            return getattr(self._lasts[-1], name)


    class Message(object):
        """
        Object for current topic message in condition expressions.

        - value in msg -> whether any message field contains value
        - msg.x        -> attribute x of message
        """

        def __init__(self, msg):
            self._msg = msg
            self._fulltext = None

        def __contains__(self, item):
            """Returns whether value exists in any message field."""
            if not self._fulltext:
                self._fulltext = "\n".join("%s" % (v, ) for _, v, _ in
                                           api.iter_message_fields(self._msg, flat=True))
            value = item if isinstance(item, six.text_type) else \
                    item.decode() if isinstance(item, six.binary_type) else str(item)
            return re.search(re.escape(value), self._fulltext, re.I)

        def __getattr__(self, name):
            """Returns attribute value of message."""
            return getattr(self._msg, name)


    class Empty(object):
        """Placeholder falsy object that raises NoMessageException on attribute access."""
        def __getattr__(self, name):  raise ConditionMixin.NoMessageException()
        def __bool__(self):           return False
        def __nonzero__(self):        return False
        def __contains__(self, item): return False
        def __len__(self):            return 0


    def __init__(self, args=None, **kwargs):
        """
        @param   args             arguments as namespace or dictionary, case-insensitive
        @param   args.condition   Python expressions that must evaluate as true
                                  for message to be processable, see ConditionMixin
        @param   kwargs           any and all arguments as keyword overrides, case-insensitive
        """
        self._topic_states         = {}  # {topic: whether only used for condition, not matching}
        self._topics_per_condition = []  # [[topics in 1st condition], ]
        self._wildcard_topics      = {}  # {"/my/*/topic": re.Pattern}
        # {(topic, typename, typehash): [1st, 2nd, ..]}
        self._firstmsgs = collections.defaultdict(collections.deque)
        # {(topic, typename, typehash): [.., last]}
        self._lastmsgs  = collections.defaultdict(collections.deque)
        # {topic: (max positive index + 1, max abs(negative index) or 1)}
        self._topic_limits = collections.defaultdict(lambda: [1, 1])

        ## {condition with <topic x> as get_topic("x"): compiled code object}
        self._conditions = collections.OrderedDict()

    def is_processable(self, topic, msg, stamp, index=None):
        """Returns whether message passes passes current state conditions, if any."""
        result = True
        if not self._conditions:
            return result
        for i, (expr, code) in enumerate(self._conditions.items()):
            topics = self._topics_per_condition[i]
            wildcarded = [t for t in topics if t in self._wildcard_topics]
            realcarded = {wt: [(t, n, h) for (t, n, h) in self._lastmsgs if p.match(t)]
                          for wt in wildcarded for p in [self._wildcard_topics[wt]]}
            variants = [[(wt, (t, n, h)) for (t, n, h) in tt] or [(wt, (wt, None))]
                        for wt, tt in realcarded.items()]
            variants = variants or [[None]]  # Ensure one iteration if no wildcards to combine

            result = False
            for remaps in itertools.product(*variants):  # [(wildcard1, realname1), (wildcard2, ..]
                if remaps == (None, ): remaps = ()
                getter = functools.partial(self._get_topic_instance, remap=dict(remaps))
                ns = {"topic": topic, "msg": ConditionMixin.Message(msg), "get_topic": getter}
                try:   result = eval(code, ns)
                except self.NoMessageException: pass
                except Exception as e:
                    ConsolePrinter.error('Error evaluating condition "%s": %s', expr, e)
                    raise
                if result: break  # for remaps
            if not result: break  # for i,
        return result

    def validate(self):
        """Returns whether conditions have valid syntax, sets options, prints errors."""
        errors = []
        for v in self.args.CONDITION:
            v = self.TOPIC_RGX.sub("dummy", v)
            try: compile(v, "", "eval")
            except SyntaxError as e:
                errors.append("'%s': %s at %schar %s" %
                              (v, e.msg, "line %s " % e.lineno if e.lineno > 1 else "", e.offset))
            except Exception as e:
                errors.append("'%s': %s" % (v, e))
        if errors:
            ConsolePrinter.error("Invalid condition")
            for err in errors:
                ConsolePrinter.error("  %s" % err)
        else:
            self._configure_conditions(ensure_namespace(self.args, ConditionMixin.DEFAULT_ARGS))
        return not errors

    def close_batch(self):
        """Clears cached messages."""
        self._firstmsgs.clear()
        self._lastmsgs.clear()

    def has_conditions(self):
        """Returns whether there are any conditions configured."""
        return bool(self._conditions)

    def conditions_get_topics(self):
        """Returns a list of all topics used in conditions (may contain wildcards)."""
        return list(self._topic_states)

    def is_conditions_topic(self, topic, pure=True):
        """
        Returns whether topic is used for checking condition.

        @param   pure  whether use should be solely for condition, not for matching at all
        """
        if not self._conditions: return False
        if topic in self._topic_states:
            return self._topic_states[topic] if pure else True
        wildcarded = [t for t, p in self._wildcard_topics.items() if p.match(topic)]
        if not wildcarded: return False
        return all(map(self._topic_states.get, wildcarded)) if pure else True

    def conditions_set_topic_state(self, topic, pure):
        """Sets whether topic is purely used for conditions not matching."""
        if topic in self._topic_states:
            self._topic_states[topic] = pure

    def conditions_register_message(self, topic, msg):
        """Retains message for condition evaluation if in condition topic."""
        if self.is_conditions_topic(topic, pure=False):
            topickey = api.TypeMeta.make(msg, topic).topickey
            self._lastmsgs[topickey].append(msg)
            if len(self._lastmsgs[topickey]) > self._topic_limits[topic][-1]:
                self._lastmsgs[topickey].popleft()
            if len(self._firstmsgs[topickey]) < self._topic_limits[topic][0]:
                self._firstmsgs[topickey].append(msg)

    def _get_topic_instance(self, topic, remap=None):
        """
        Returns Topic() by name.

        @param   remap  optional remap dictionary as {topic1: (topic2, typename, typehash)}
        """
        if remap and topic in remap:
            topickey = remap[topic]
        else:
            topickey = next(((t, n, h) for (t, n, h) in self._lastmsgs if t == topic), None)
        if topickey not in self._counts:
            return self.Empty()
        c, f, l = (d[topickey] for d in (self._counts, self._firstmsgs, self._lastmsgs))
        return self.Topic(c, f, l)

    def _configure_conditions(self, args):
        """Parses condition expressions and populates local structures."""
        self._conditions.clear()
        self._topic_limits.clear()
        self._topic_states.clear()
        self._wildcard_topics.clear()
        del self._topics_per_condition[:]
        for v in args.CONDITION:
            topics = list(set(self.TOPIC_RGX.findall(v)))
            self._topic_states.update({t: True for t in topics})
            self._topics_per_condition.append(topics)
            for t in (t for t in topics if "*" in t):
                self._wildcard_topics[t] = common.wildcard_to_regex(t, end=True)
            expr = self.TOPIC_RGX.sub(r'get_topic("\1")', v)
            self._conditions[expr] = compile(expr, "", "eval")

        for v in args.CONDITION:  # Set history length from <topic x>[index]
            indexexprs = re.findall(self.TOPIC_RGX.pattern + r"\s*\[([^\]]+)\]", v)
            for topic, indexexpr in indexexprs:
                limits = self._topic_limits[topic]
                try:
                    index = eval(indexexpr)  # If integer, set history limits
                    limits[index < 0] = max(limits[index < 0], abs(index) + (index >= 0))
                except Exception: continue  # for topic


class BagSource(Source, ConditionMixin):
    """Produces messages from ROS bagfiles."""

    ## Template for message metainfo line
    MESSAGE_META_TEMPLATE = "{topic} {index}/{total} ({type}  {dt}  {stamp})"

    ## Template for bag metainfo header
    META_TEMPLATE = "\nFile {file} ({size}), {tcount} topics, {mcount:,d} messages\n" \
                    "File period {startdt} - {enddt}\n" \
                    "File span {delta} ({start} - {end})"

    ## Constructor argument defaults
    DEFAULT_ARGS = dict(BAG=(), FILE=(), PATH=(), RECURSE=False, TOPIC=(), TYPE=(),
                        SKIP_TOPIC=(), SKIP_TYPE=(), START_TIME=None, END_TIME=None,
                        START_INDEX=None, END_INDEX=None, CONDITION=(), AFTER=0, ORDERBY=None,
                        DECOMPRESS=False, REINDEX=False, WRITE=(), PROGRESS=False,
                        STOP_ON_ERROR=False, TIMESCALE=0, TIMESCALE_EMISSION=False, VERBOSE=False)

    def __init__(self, args=None, **kwargs):
        """
        @param   args                   arguments as namespace or dictionary, case-insensitive;
                                        or a single path as the ROS bagfile to read,
                                        or a stream to read from,
                                        or one or more {@link grepros.api.Bag Bag} instances
        <!--sep-->

        Bag-specific arguments:
        @param   args.file              names of ROS bagfiles to read if not all in directory,
                                        or a stream to read from;
                                        or one or more {@link grepros.api.Bag Bag} instances
        @param   args.path              paths to scan if not current directory
        @param   args.recurse           recurse into subdirectories when looking for bagfiles
        @param   args.orderby           "topic" or "type" if any to group results by
        @param   args.decompress        decompress archived bags to file directory
        @param   args.reindex           make a copy of unindexed bags and reindex them (ROS1 only)
        @param   args.timescale         emit messages on original timeline from first message
                                        at given rate, 0 disables
        @param   args.timescale_emission
                                        timeline from first matched message not first in bag,
                                        requires notify() for each message
        @param   args.write             outputs, to skip in input files
        @param   args.bag               one or more {@link grepros.api.Bag Bag} instances
        <!--sep-->

        General arguments:
        @param   args.topic             ROS topics to read if not all
        @param   args.type              ROS message types to read if not all
        @param   args.skip_topic        ROS topics to skip
        @param   args.skip_type         ROS message types to skip
        @param   args.start_time        earliest timestamp of messages to read
        @param   args.end_time          latest timestamp of messages to read
        @param   args.start_index       message index within topic to start from
        @param   args.end_index         message index within topic to stop at
        @param   args.unique            emit messages that are unique in topic
        @param   args.select_field      message fields to use for uniqueness if not all
        @param   args.noselect_field    message fields to skip for uniqueness
        @param   args.nth_message       read every Nth message in topic, starting from first
        @param   args.nth_interval      minimum time interval between messages in topic,
                                        as seconds or ROS duration
        @param   args.condition         Python expressions that must evaluate as true
                                        for message to be processable, see ConditionMixin
        @param   args.progress          whether to print progress bar
        @param   args.stop_on_error     stop execution on any error like unknown message type
        @param   args.verbose           whether to print error stacktraces
        @param   kwargs                 any and all arguments as keyword overrides, case-insensitive
        """
        args0 = args
        is_bag = isinstance(args, api.Bag) or \
                 common.is_iterable(args) and all(isinstance(x, api.Bag) for x in args)
        args = {"FILE": str(args)} if isinstance(args, common.PATH_TYPES) else \
               {"FILE": args} if common.is_stream(args) else {} if is_bag else args
        args = ensure_namespace(args, BagSource.DEFAULT_ARGS, **kwargs)
        super(BagSource, self).__init__(args)
        ConditionMixin.__init__(self, args)
        self._args0     = common.structcopy(self.args)  # Original arguments
        self._totals_ok = False  # Whether message count totals have been retrieved (ROS2 optimize)
        self._types_ok  = False  # Whether type definitions have been retrieved (ROS2 optimize)
        self._running   = False
        self._bag       = None   # Current bag object instance
        self._filename  = None   # Current bagfile path
        self._meta      = None   # Cached get_meta()
        self._bag0      = ([args0] if isinstance(args0, api.Bag) else args0) if is_bag else None
        self._delaystamps = collections.defaultdict(int)  # Tracked timestamps for timeline emission

    def read(self):
        """Yields messages from ROS bagfiles, as (topic, msg, ROS time)."""
        if not self.validate(): raise Exception("invalid")
        self._running = True

        for _ in self._produce_bags():
            if not self._running:
                break  # for _

            topicsets = [self._topics]
            if "topic" == self.args.ORDERBY:  # Group output by sorted topic names
                topicsets = [{n: tt} for n, tt in sorted(self._topics.items())]
            elif "type" == self.args.ORDERBY:  # Group output by sorted type names
                typetopics = {}
                for n, tt in self._topics.items():
                    for t in tt: typetopics.setdefault(t, []).append(n)
                topicsets = [{n: [t] for n in nn} for t, nn in sorted(typetopics.items())]

            self._types_ok = False
            self.init_progress()
            for topics in topicsets:
                for topic, msg, stamp, index in self._produce(topics) if topics else ():
                    self.conditions_register_message(topic, msg)
                    if not self.is_conditions_topic(topic, pure=True) \
                    and (not self.preprocess or self.is_processable(topic, msg, stamp, index)):
                        yield self.SourceMessage(topic, msg, stamp)
                if not self._running:
                    break  # for topics
            self._counts and self.sink and self.sink.flush()
            self.close_batch()
        self._running = False

    def configure(self, args=None, **kwargs):
        """
        Updates source configuration.

        @param   args    arguments as namespace or dictionary, case-insensitive
        @param   kwargs  any and all arguments as keyword overrides, case-insensitive
        """
        super(BagSource, self).configure(args, **kwargs)
        self._args0 = common.structcopy(self.args)

    def validate(self):
        """Returns whether ROS environment is set and arguments valid, prints error if not."""
        if self.valid is not None: return self.valid
        self.valid = Source.validate(self)
        if not api.validate():
            self.valid = False
        if not self._bag0 and self.args.FILE and os.path.isfile(self.args.FILE[0]) \
        and not common.verify_io(self.args.FILE[0], "r"):
            ConsolePrinter.error("File not readable.")
            self.valid = False
        if not self._bag0 and common.is_stream(self.args.FILE) \
        and not any(c.STREAMABLE for c in api.Bag.READER_CLASSES):
            ConsolePrinter.error("Bag format does not support reading streams.")
            self.valid = False
        if self._bag0 and not any(x.mode in ("r", "a") for x in self._bag0):
            ConsolePrinter.error("Bag not in read mode.")
            self.valid = False
        if self.args.ORDERBY and self.conditions_get_topics():
            ConsolePrinter.error("Cannot use topics in conditions and bag order by %s.",
                                 self.args.ORDERBY)
            self.valid = False
        if self.args.TIMESCALE and self.args.TIMESCALE < 0:
            ConsolePrinter.error("Invalid timescale factor: %r.", self.args.TIMESCALE)
            self.valid = False
        if not ConditionMixin.validate(self):
            self.valid = False
        return self.valid

    def close(self):
        """Closes current bag, if any."""
        self._running = False
        if self._bag and not self._bag0: self._bag.close()
        ConditionMixin.close_batch(self)
        super(BagSource, self).close()

    def close_batch(self):
        """Closes current bag, if any."""
        if self._bag0: self._running = False
        elif self._bag: self._bag.close()
        self._bag = None
        if self.bar:
            self.bar.update(flush=True)
            self.bar = None
            if self._bar_args.get("source_value") is not None:
                self._bar_args["source_value"] = 0
        ConditionMixin.close_batch(self)

    def format_meta(self):
        """Returns bagfile metainfo string."""
        return self.META_TEMPLATE.format(**self.get_meta())

    def format_message_meta(self, topic, msg, stamp, index=None):
        """Returns message metainfo string."""
        meta = self.get_message_meta(topic, msg, stamp, index)
        meta = {k: "" if v is None else v for k, v in meta.items()}
        return self.MESSAGE_META_TEMPLATE.format(**meta)

    def get_batch(self):
        """Returns name of current bagfile, or self if reading stream."""
        return self._filename if self._filename is not None else self

    def get_meta(self):
        """Returns bagfile metainfo data dict."""
        if self._meta is not None:
            return self._meta
        mcount = self._bag.get_message_count()
        start, end = (self._bag.get_start_time(), self._bag.get_end_time()) if mcount else ("", "")
        delta = common.format_timedelta(datetime.timedelta(seconds=(end or 0) - (start or 0)))
        self._meta = dict(file=self._filename, size=common.format_bytes(self._bag.size),
                          mcount=mcount, tcount=len(self.topics), delta=delta,
                          start=drop_zeros(start), end=drop_zeros(end),
                          startdt=drop_zeros(common.format_stamp(start)) if start != "" else "",
                          enddt=drop_zeros(common.format_stamp(end)) if end != "" else "")
        return self._meta

    def get_message_meta(self, topic, msg, stamp, index=None):
        """Returns message metainfo data dict."""
        self._ensure_totals()
        result = super(BagSource, self).get_message_meta(topic, msg, stamp, index)
        result.update(total=self.topics[(topic, result["type"], result["hash"])])
        if callable(getattr(self._bag, "get_qoses", None)):
            result.update(qoses=self._bag.get_qoses(topic, result["type"]))
        return result

    def get_message_class(self, typename, typehash=None):
        """Returns ROS message type class."""
        return self._bag.get_message_class(typename, typehash) or \
               api.get_message_class(typename)

    def get_message_definition(self, msg_or_type):
        """Returns ROS message type definition full text, including subtype definitions."""
        return self._bag.get_message_definition(msg_or_type) or \
               api.get_message_definition(msg_or_type)

    def get_message_type_hash(self, msg_or_type):
        """Returns ROS message type MD5 hash."""
        return self._bag.get_message_type_hash(msg_or_type) or \
               api.get_message_type_hash(msg_or_type)

    def notify(self, status):
        """Reports match status of last produced message."""
        super(BagSource, self).notify(status)
        if status and not self._totals_ok:
            self._ensure_totals()
        if status and self.args.TIMESCALE and self.args.TIMESCALE_EMISSION:
            if "first" not in self._delaystamps:
                self._delaystamps["first"] = self._delaystamps["current"]
            else: self._delay_timeline()  # Delay until time met

    def is_processable(self, topic, msg, stamp, index=None):
        """Returns whether message passes source filters; registers status."""
        self._status = False
        topickey = api.TypeMeta.make(msg, topic).topickey
        if self.args.START_INDEX and index is not None and self.args.START_INDEX < 0 \
        and topickey not in self._start_indexes:  # Populate topic in _start_indexes
            self._ensure_totals()
            self._start_indexes[topickey] = max(0, self.args.START_INDEX + self.topics[topickey])
        if self.args.END_INDEX and index is not None and self.args.END_INDEX < 0 \
        and topickey not in self._end_indexes:  # Populate topic in _end_indexes
            self._ensure_totals()
            self._end_indexes[topickey] = (self.args.END_INDEX + self.topics[topickey])
            if not self._end_indexes[topickey]: self._end_indexes[topickey] = -1

        if not super(BagSource, self).is_processable(topic, msg, stamp, index):
            return False
        if not ConditionMixin.is_processable(self, topic, msg, stamp, index):
            return False
        self._status = True
        return True

    def init_progress(self):
        """Initializes progress bar, if any, for current bag."""
        if self.args.PROGRESS and not self.bar:
            self._ensure_totals()
            self.configure_progress(**self._make_progress_args())
            super(BagSource, self).init_progress()

    def _produce(self, topics, start_time=None):
        """
        Yields messages from current ROS bagfile, as (topic, msg, ROS time, index in topic).

        @param   topics  {topic: [typename, ]}
        """
        if not self._running or not self._bag: return
        do_predelay = self.args.TIMESCALE and not self.args.TIMESCALE_EMISSION
        if do_predelay: self._delaystamps["first"] = self._bag.get_start_time()
        if self.args.TIMESCALE and "read" not in self._delaystamps:
            self._delaystamps["read"] = getattr(time, "monotonic", time.time)()  # Py3 / Py2
        counts = collections.Counter()
        endtime_indexes = {}  # {topickey: index at reaching END_TIME}
        nametypes = {(n, t) for n, tt in topics.items() for t in tt}
        for topic, msg, stamp in self._bag.read_messages(list(topics), start_time):
            if not self._running or not self._bag:
                break  # for topic,
            typename = api.get_message_type(msg)
            if topics and typename not in topics[topic]:
                continue  # for topic,
            if api.ROS2 and not self._types_ok:
                self.topics, self._types_ok = self._bag.get_topic_info(counts=False), True

            topickey = api.TypeMeta.make(msg, topic, self).topickey
            counts[topickey] += 1; self._counts[topickey] += 1
            # Skip messages already processed during sticky
            if start_time is None and counts[topickey] != self._counts[topickey]:
                continue  # for topic,

            self._status, self._delaystamps["current"] = None, api.to_sec(stamp)
            if do_predelay: self._delay_timeline()  # Delay emission until time
            if self.bar: self.update_progress(sum(self._counts.values()))
            yield topic, msg, stamp, self._counts[topickey]

            if self._status:
                self._processables[topickey] = (self._counts[topickey], stamp)
            if self._status and not self.preprocess and self.args.AFTER and start_time is None \
            and not self.has_conditions() \
            and (len(self._topics) > 1 or len(next(iter(self._topics.values()))) > 1):
                # Stick to one topic until trailing messages have been emitted
                for entry in self._produce({topic: typename}, stamp + api.make_duration(nsecs=1)):
                    yield entry
            if not self._running or not self._bag or (start_time is None
            and self._is_at_end_threshold(topickey, stamp, nametypes, endtime_indexes)):
                break  # for topic,

    def _produce_bags(self):
        """Yields Bag instances from configured arguments."""
        if self._bag0:
            for bag in self._bag0:
                if self._configure(bag=bag):
                    yield self._bag
            return

        names, paths = self.args.FILE, self.args.PATH
        exts, skip_exts = api.BAG_EXTENSIONS, api.SKIP_EXTENSIONS
        exts = list(exts) + ["%s%s" % (a, b) for a in exts for b in common.Decompressor.EXTENSIONS]

        encountereds = set()
        for filename in common.find_files(names, paths, exts, skip_exts, self.args.RECURSE):
            if not self._running:
                break  # for filename

            fullname = os.path.realpath(os.path.abspath(filename))
            skip = common.Decompressor.make_decompressed_name(fullname) in encountereds
            encountereds.add(fullname)

            if skip or not self._configure(filename):
                continue  # for filename

            encountereds.add(self._bag.filename)
            yield self._bag

    def _make_progress_args(self):
        """Returns dictionary with progress bar options"""
        total = sum(sum(c for (t, n, _), c in self.topics.items() if c and t == t_ and n in nn)
                    for t_, nn in self._topics.items())
        result = dict(max=total, afterword=os.path.basename(self._filename or "<stream>"))

        instr, outstr = "{value:,d}/{max:,d}", ""
        if any([self.args.CONDITION, self.args.UNIQUE, self.args.NTH_INTERVAL,
                self.args.START_TIME, self.args.END_TIME]) or self.args.NTH_MESSAGE > 1:
            self._bar_args.setdefault("source_value", 0)  # Separate counts if not all messages
        if self._bar_args.get("source_value") is not None \
        or self._bar_args.get("match_max") is not None:
            result.update(source_value=self._bar_args.get("source_value") or 0)
            instr, outstr = "{source_value:,d}/{max:,d}", "matched {value:,d}"
            if self._bar_args.get("match_max") is not None:
                instr, outstr = "{source_value:,d}/{source_max:,d}", outstr + "/{match_max:,d}"
                result.update(source_max=total, max=min(total, self._bar_args["match_max"]))
        result.update(aftertemplate=" {afterword} (%s)" % "  ".join(filter(bool, (instr, outstr))))

        return result

    def _ensure_totals(self):
        """Retrieves total message counts if not retrieved."""
        if not self._totals_ok:  # ROS2 bag probably
            has_ensure = common.has_arg(self._bag.get_topic_info, "ensure_types")
            kws = dict(ensure_types=False) if has_ensure else {}
            for (t, n, h), c in self._bag.get_topic_info(**kws).items():
                self.topics[(t, n, h)] = c
            self._totals_ok = True

    def _delay_timeline(self):
        """Sleeps until message ought to be emitted in bag timeline."""
        curstamp, readstamp, startstamp = map(self._delaystamps.get, ("current", "read", "first"))
        delta = max(0, api.to_sec(curstamp) - startstamp) / (self.args.TIMESCALE or 1)
        if delta: time.sleep(max(0, delta + readstamp - getattr(time, "monotonic", time.time)()))

    def _is_at_end_threshold(self, topickey, stamp, nametypes, endtime_indexes):
        """
        Returns whether bag reading has reached END_INDEX or END_TIME in all given topics.

        @param   topickey         (topic, typename, typehash) of current message
        @param   stamp            ROS timestamp of current message
        @param   nametypes        {(topic, typename)} to account for
        @param   endtime_indexes  {topickey: index at reaching END_TIME}, gets modified
        """
        if self.args.END_INDEX:
            max_index = self.args.END_INDEX + self.args.AFTER
            if self._counts[topickey] >= max_index:  # Stop reading when reaching max in all topics
                mycounts = {k: v for k, v in self._counts.items() if k[:2] in nametypes}
                if nametypes == set(k[:2] for k in mycounts) \
                and all(v >= self._end_indexes.get(k, max_index) for k, v in mycounts.items()):
                    return True  # Early break if all topics at max index
        if self.args.END_TIME and stamp > self.args.END_TIME:
            self._ensure_totals()
            if topickey not in endtime_indexes: endtime_indexes[topickey] = self._counts[topickey]
            max_index = min(self.topics[topickey], endtime_indexes[topickey] + self.args.AFTER)
            if self._counts[topickey] >= max_index: # One topic reached end: check all topics
                myindexes = {k: v for k, v in endtime_indexes.items() if k[:2] in nametypes}
                if nametypes == set(k[:2] for k in myindexes) \
                and all(self._counts[k] >= min(self.topics[k], v + self.args.AFTER)
                        for k, v in myindexes.items()):
                    return True  # Early break if all topics at max time
        return False

    def _configure(self, filename=None, bag=None):
        """Opens bag and populates bag-specific argument state, returns success."""
        self._meta      = None
        self._bag       = None
        self._filename  = None
        self._totals_ok = False
        self._delaystamps.clear()
        self._counts.clear()
        self._start_indexes.clear()
        self._end_indexes.clear()
        self._processables.clear()
        self._hashes.clear()
        self.topics.clear()

        if bag is not None and bag.mode not in ("r", "a"):
            ConsolePrinter.warn("Cannot read %s: bag in write mode.", bag)
            return False

        if filename and self.args.WRITE \
        and any(os.path.realpath(x[0]) == os.path.realpath(filename)
                for x in self.args.WRITE):
            return False
        try:
            if filename and common.Decompressor.is_compressed(filename):
                if self.args.DECOMPRESS:
                    filename = common.Decompressor.decompress(filename, self.args.PROGRESS)
                else: raise Exception("decompression not enabled")
            bag = api.Bag(filename, mode="r", reindex=self.args.REINDEX,
                          progress=self.args.PROGRESS) if bag is None else bag
            bag.stop_on_error = self.args.STOP_ON_ERROR
            bag.open()
        except Exception as e:
            ConsolePrinter.error("\nError opening %r: %s", filename or bag, e)
            if self.args.STOP_ON_ERROR: raise
            if self.args.VERBOSE: traceback.print_exc()
            return False

        self._bag      = bag
        self._filename = bag.filename

        dct = fulldct = {}  # {topic: [typename, ]}
        kws = dict(ensure_types=False) if common.has_arg(bag.get_topic_info, "ensure_types") else {}
        for (t, n, h), c in bag.get_topic_info(counts=False, **kws).items():
            dct.setdefault(t, []).append(n)
            self.topics[(t, n, h)] = c
        self._totals_ok = not any(v is None for v in self.topics.values())
        for topic in self.conditions_get_topics():
            self.conditions_set_topic_state(topic, True)

        dct = common.filter_dict(dct, self.args.TOPIC, self.args.TYPE)
        dct = common.filter_dict(dct, self.args.SKIP_TOPIC, self.args.SKIP_TYPE, reverse=True)
        for topic in self.conditions_get_topics():  # Add topics used in conditions
            matches = [t for p in [common.wildcard_to_regex(topic, end=True)] for t in fulldct
                       if t == topic or "*" in topic and p.match(t)]
            for realtopic in matches:
                self.conditions_set_topic_state(realtopic, realtopic not in dct)
                dct.setdefault(realtopic, fulldct[realtopic])
        self._topics = dct
        self._meta   = self.get_meta()

        args = self.args = common.structcopy(self._args0)
        if args.START_TIME is not None:
            args.START_TIME = api.make_bag_time(args.START_TIME, bag)
        if args.END_TIME is not None:
            args.END_TIME = api.make_bag_time(args.END_TIME, bag)
        return True


class LiveSource(Source, ConditionMixin):
    """Produces messages from live ROS topics."""

    ## Seconds between refreshing available topics from ROS master.
    MASTER_INTERVAL = 2

    ## Constructor argument defaults
    DEFAULT_ARGS = dict(TOPIC=(), TYPE=(), SKIP_TOPIC=(), SKIP_TYPE=(), START_TIME=None,
                        END_TIME=None, START_INDEX=None, END_INDEX=None, CONDITION=(),
                        QUEUE_SIZE_IN=10, ROS_TIME_IN=False, PROGRESS=False, STOP_ON_ERROR=False,
                        VERBOSE=False)

    def __init__(self, args=None, **kwargs):
        """
        @param   args                   arguments as namespace or dictionary, case-insensitive
        @param   args.topic             ROS topics to read if not all
        @param   args.type              ROS message types to read if not all
        @param   args.skip_topic        ROS topics to skip
        @param   args.skip_type         ROS message types to skip
        @param   args.start_time        earliest timestamp of messages to read
        @param   args.end_time          latest timestamp of messages to read
        @param   args.start_index       message index within topic to start from
        @param   args.end_index         message index within topic to stop at
        @param   args.unique            emit messages that are unique in topic
        @param   args.select_field      message fields to use for uniqueness if not all
        @param   args.noselect_field    message fields to skip for uniqueness
        @param   args.nth_message       read every Nth message in topic, starting from first
        @param   args.nth_interval      minimum time interval between messages in topic,
                                        as seconds or ROS duration
        @param   args.condition         Python expressions that must evaluate as true
                                        for message to be processable, see ConditionMixin
        @param   args.queue_size_in     subscriber queue size (default 10)
        @param   args.ros_time_in       stamp messages with ROS time instead of wall time
        @param   args.progress          whether to print progress bar
        @param   args.stop_on_error     stop execution on any error like unknown message type
        @param   args.verbose           whether to print error stacktraces
        @param   kwargs                 any and all arguments as keyword overrides, case-insensitive
        """
        args = ensure_namespace(args, LiveSource.DEFAULT_ARGS, **dict(kwargs, live=True))
        super(LiveSource, self).__init__(args)
        ConditionMixin.__init__(self, args)
        self._running    = False  # Whether is in process of yielding messages from topics
        self._queue      = None   # [(topic, msg, ROS time)]
        self._last_stamp = None   # ROS stamp of last message
        self._subs       = {}     # {(topic, typename, typehash): ROS subscriber}

    def read(self):
        """Yields messages from subscribed ROS topics, as (topic, msg, ROS time)."""
        if not self._running:
            if not self.validate(): raise Exception("invalid")
            api.init_node()
            self._running = True
            self._queue = queue.Queue()
            self.refresh_topics()
            t = threading.Thread(target=self._run_refresh)
            t.daemon = True
            t.start()
            if self.args.END_TIME:
                self._last_stamp = None
                t = threading.Thread(target=self._run_endtime_closer)
                t.daemon = True
                t.start()

        total = 0
        self.init_progress()
        while self._running:
            topic, msg, stamp = self._queue.get()
            total += bool(topic)
            self.update_progress(total, running=self._running and bool(topic))
            if not topic: continue  # while

            topickey = api.TypeMeta.make(msg, topic, self).topickey
            self._counts[topickey] += 1
            self._last_stamp = stamp
            self.conditions_register_message(topic, msg)
            if self.is_conditions_topic(topic, pure=True): continue  # while

            self._status = None
            if not self.preprocess \
            or self.is_processable(topic, msg, stamp, self._counts[topickey]):
                yield self.SourceMessage(topic, msg, stamp)
            if self._status and (self.args.NTH_MESSAGE > 1 or self.args.NTH_INTERVAL > 0):
                self._processables[topickey] = (self._counts[topickey], stamp)
        self._queue = None
        self._running = False

    def bind(self, sink):
        """Attaches sink to source and blocks until connected to ROS live."""
        if not self.validate(): raise Exception("invalid")
        super(LiveSource, self).bind(sink)
        api.init_node()

    def validate(self):
        """Returns whether ROS environment is set and arguments valid, prints error if not."""
        if self.valid is not None: return self.valid
        self.valid = Source.validate(self)
        if not api.validate(live=True):
            self.valid = False
        if not ConditionMixin.validate(self):
            self.valid = False
        if self.valid:
            self._configure()
        return self.valid

    def close(self):
        """Shuts down subscribers and stops producing messages."""
        self._running = False
        for k in list(self._subs):
            self._subs.pop(k).unregister()
        self._queue and self._queue.put((None, None, None))  # Wake up iterator
        self._queue = None
        ConditionMixin.close_batch(self)
        super(LiveSource, self).close()

    def get_meta(self):
        """Returns source metainfo data dict."""
        ENV = {k: os.getenv(k) for k in ("ROS_MASTER_URI", "ROS_DOMAIN_ID") if os.getenv(k)}
        return dict(ENV, tcount=len(self.topics), scount=len(self._subs))

    def get_message_meta(self, topic, msg, stamp, index=None):
        """Returns message metainfo data dict."""
        result = super(LiveSource, self).get_message_meta(topic, msg, stamp, index)
        topickey = (topic, result["type"], result["hash"])
        if topickey in self._subs:
            result.update(qoses=self._subs[topickey].get_qoses())
        return result

    def get_message_class(self, typename, typehash=None):
        """Returns message type class, from active subscription if available."""
        sub = next((s for (t, n, h), s in self._subs.items()
                    if n == typename and typehash in (s.get_message_type_hash(), None)), None)
        return sub and sub.get_message_class() or api.get_message_class(typename)

    def get_message_definition(self, msg_or_type):
        """Returns ROS message type definition full text, including subtype definitions."""
        if api.is_ros_message(msg_or_type):
            return api.get_message_definition(msg_or_type)
        sub = next((s for (t, n, h), s in self._subs.items() if n == msg_or_type), None)
        return sub and sub.get_message_definition() or api.get_message_definition(msg_or_type)

    def get_message_type_hash(self, msg_or_type):
        """Returns ROS message type MD5 hash."""
        if api.is_ros_message(msg_or_type):
            return api.get_message_type_hash(msg_or_type)
        sub = next((s for (t, n, h), s in self._subs.items() if n == msg_or_type), None)
        return sub and sub.get_message_type_hash() or api.get_message_type_hash(msg_or_type)

    def format_meta(self):
        """Returns source metainfo string."""
        metadata = self.get_meta()
        result = "\nROS%s live" % api.ROS_VERSION
        if "ROS_MASTER_URI" in metadata:
            result += ", ROS master %s" % metadata["ROS_MASTER_URI"]
        if "ROS_DOMAIN_ID" in metadata:
            result += ", ROS domain ID %s" % metadata["ROS_DOMAIN_ID"]
        result += ", %s initially" % common.plural("topic", metadata["tcount"])
        result += ", %s subscribed" % metadata["scount"]
        return result

    def is_processable(self, topic, msg, stamp, index=None):
        """Returns whether message passes source filters; registers status."""
        self._status = False
        if not super(LiveSource, self).is_processable(topic, msg, stamp, index):
            return False
        if not ConditionMixin.is_processable(self, topic, msg, stamp, index):
            return False
        self._status = True
        return True

    def refresh_topics(self):
        """Refreshes topics and subscriptions from ROS live."""
        for topic, typename in api.get_topic_types():
            topickey = (topic, typename, None)
            self.topics[topickey] = None
            dct = common.filter_dict({topic: [typename]}, self.args.TOPIC, self.args.TYPE)
            if not common.filter_dict(dct, self.args.SKIP_TOPIC, self.args.SKIP_TYPE, reverse=True):
                continue  # for topic, typename
            if api.ROS2 and api.get_message_class(typename) is None:
                msg = "Error loading type %s in topic %s." % (typename, topic)
                if self.args.STOP_ON_ERROR: raise Exception(msg)
                ConsolePrinter.warn(msg, __once=True)
                continue  # for topic, typename
            if topickey in self._subs:
                continue  # for topic, typename

            handler = functools.partial(self._on_message, topic)
            try:
                sub = api.create_subscriber(topic, typename, handler,
                                            queue_size=self.args.QUEUE_SIZE_IN)
            except Exception as e:
                ConsolePrinter.warn("Error subscribing to topic %s: %%r" % topic,
                                    e, __once=True)
                if self.args.STOP_ON_ERROR: raise
                if self.args.VERBOSE: traceback.print_exc()
                continue  # for topic, typename
            self._subs[topickey] = sub

    def init_progress(self):
        """Initializes progress bar, if any."""
        if self.args.PROGRESS and not self.bar:
            self.configure_progress(**self._make_progress_args())
            super(LiveSource, self).init_progress()

    def update_progress(self, count, running=True):
        """Updates progress bar, if any."""
        if self.bar:
            if count in (1, 2):  # Change plurality
                self.configure_progress(**self._make_progress_args(count))
            super(LiveSource, self).update_progress(count, running)

    def _configure(self):
        """Adjusts start/end time filter values to current time."""
        if self.args.START_TIME is not None:
            self.args.START_TIME = api.make_live_time(self.args.START_TIME)
        if self.args.END_TIME is not None:
            self.args.END_TIME = api.make_live_time(self.args.END_TIME)

    def _make_progress_args(self, count=None):
        """Returns dictionary with progress bar options, for specific nessage index if any."""
        result = dict(afterword = "ROS%s live" % api.ROS_VERSION, pulse=True)
        if self._bar_args.get("match_max") is not None:
            result.update(max=self._bar_args["match_max"], pulse=False)

        instr, outstr = "{value:,d} message%s" % ("" if count == 1 else "s"), ""
        if any([self.args.CONDITION, self.args.UNIQUE, self.args.NTH_INTERVAL,
                self.args.START_TIME, self.args.END_TIME]) or self.args.NTH_MESSAGE > 1:
            self._bar_args.setdefault("source_value", 0)  # Separate counts if not all messages
        if self._bar_args.get("source_value") is not None:
            instr = "{source_value:,d} message%s" % ("" if count == 1 else "s")
            outstr = "matched {value:,d}"
            if self._bar_args.get("match_max") is not None: outstr += "/{match_max:,d}"
        elif self._bar_args.get("match_max") is not None:
            instr = "{value:,d}/{max:,d}"
        result.update(aftertemplate=" {afterword} (%s)" % "  ".join(filter(bool, (instr, outstr))))

        return result

    def _run_refresh(self):
        """Periodically refreshes topics and subscriptions from ROS live."""
        time.sleep(self.MASTER_INTERVAL)
        while self._running:
            try: self.refresh_topics()
            except Exception as e: self.thread_excepthook("Error refreshing live topics: %r" % e, e)
            time.sleep(self.MASTER_INTERVAL)

    def _run_endtime_closer(self):
        """Periodically checks whether END_TIME has been reached, closes source when so."""
        time.sleep(self.MASTER_INTERVAL)
        while self._running and self.args.END_TIME:
            if self._last_stamp and self._last_stamp > self.args.END_TIME:
                time.sleep(self.MASTER_INTERVAL)  # Allow some more arrivals just in case
                self.close()
            else: time.sleep(self.MASTER_INTERVAL)

    def _on_message(self, topic, msg):
        """Subscription callback handler, queues message for yielding."""
        stamp = api.get_rostime() if self.args.ROS_TIME_IN else api.make_time(time.time())
        self._queue and self._queue.put((topic, msg, stamp))


class AppSource(Source, ConditionMixin):
    """Produces messages from iterable or pushed data."""

    ## Constructor argument defaults
    DEFAULT_ARGS = dict(TOPIC=(), TYPE=(), SKIP_TOPIC=(), SKIP_TYPE=(), START_TIME=None,
                        END_TIME=None, START_INDEX=None, END_INDEX=None, UNIQUE=False,
                        SELECT_FIELD=(), NOSELECT_FIELD=(), NTH_MESSAGE=1, NTH_INTERVAL=0,
                        CONDITION=(), ITERABLE=None)

    def __init__(self, args=None, **kwargs):
        """
        @param   args                  arguments as namespace or dictionary, case-insensitive;
                                       or iterable yielding messages
        @param   args.topic            ROS topics to read if not all
        @param   args.type             ROS message types to read if not all
        @param   args.skip_topic       ROS topics to skip
        @param   args.skip_type        ROS message types to skip
        @param   args.start_time       earliest timestamp of messages to read
        @param   args.end_time         latest timestamp of messages to read
        @param   args.start_index      message index within topic to start from
        @param   args.end_index        message index within topic to stop at
        @param   args.unique           emit messages that are unique in topic
        @param   args.select_field     message fields to use for uniqueness if not all
        @param   args.noselect_field   message fields to skip for uniqueness
        @param   args.nth_message      read every Nth message in topic, starting from first
        @param   args.nth_interval     minimum time interval between messages in topic,
                                       as seconds or ROS duration
        @param   args.condition        Python expressions that must evaluate as true
                                       for message to be processable, see ConditionMixin
        @param   args.iterable         iterable yielding (topic, msg, stamp) or (topic, msg);
                                       yielding `None` signals end of content
        @param   kwargs                any and all arguments as keyword overrides, case-insensitive
        """
        if common.is_iterable(args) and not isinstance(args, dict):
            args = ensure_namespace(None, iterable=args)
        args = ensure_namespace(args, AppSource.DEFAULT_ARGS, **kwargs)
        super(AppSource, self).__init__(args)
        ConditionMixin.__init__(self, args)
        self._queue = queue.Queue()  # [(topic, msg, ROS time)]
        self._reading = False

    def read(self):
        """
        Yields messages from iterable or pushed data, as (topic, msg, ROS timestamp).

        Blocks until a message is available, or source is closed.
        """
        if not self.validate(): raise Exception("invalid")
        def generate(iterable):
            for x in iterable: yield x
        feeder = generate(self.args.ITERABLE) if self.args.ITERABLE else None
        self._reading = True
        while self._reading:
            item = self._queue.get() if not feeder or self._queue.qsize() else next(feeder, None)
            if item is None: break  # while

            if len(item) > 2: topic, msg, stamp = item[:3]
            else: (topic, msg), stamp = item[:2], api.get_rostime(fallback=True)
            topickey = api.TypeMeta.make(msg, topic, self).topickey
            self._counts[topickey] += 1
            self.conditions_register_message(topic, msg)
            if self.is_conditions_topic(topic, pure=True): continue  # while

            self._status = None
            if not self.preprocess \
            or self.is_processable(topic, msg, stamp, self._counts[topickey]):
                yield self.SourceMessage(topic, msg, stamp)
            if self._status and (self.args.NTH_MESSAGE > 1 or self.args.NTH_INTERVAL > 0):
                self._processables[topickey] = (self._counts[topickey], stamp)
        self._reading = False

    def close(self):
        """Closes current read() yielding, if any."""
        if self._reading:
            self._reading = False
            self._queue.put(None)

    def read_queue(self):
        """
        Returns (topic, msg, stamp) from push queue, or `None` if no queue
        or message in queue is condition topic only.
        """
        if not self.validate(): raise Exception("invalid")
        item = None
        try: item = self._queue.get(block=False)
        except queue.Empty: pass
        if item is None: return None

        topic, msg, stamp = item
        topickey = api.TypeMeta.make(msg, topic, self).topickey
        self._counts[topickey] += 1
        self.conditions_register_message(topic, msg)
        return None if self.is_conditions_topic(topic, pure=True) else (topic, msg, stamp)

    def mark_queue(self, topic, msg, stamp):
        """Registers message produced from read_queue()."""
        if not self.validate(): raise Exception("invalid")
        if self.args.NTH_MESSAGE > 1 or self.args.NTH_INTERVAL > 0:
            topickey = api.TypeMeta.make(msg, topic).topickey
            self._processables[topickey] = (self._counts[topickey], stamp)

    def push(self, topic, msg=None, stamp=None):
        """
        Pushes a message to be yielded from read().

        @param   topic  topic name, or `None` to signal end of content
        @param   msg    ROS message
        @param   stamp  message ROS timestamp, defaults to current wall time if `None`
        """
        if not self.validate(): raise Exception("invalid")
        if topic is None: self._queue.put(None)
        else: self._queue.put((topic, msg, stamp or api.get_rostime(fallback=True)))

    def is_processable(self, topic, msg, stamp, index=None):
        """Returns whether message passes source filters; registers status."""
        self._status = False
        dct = common.filter_dict({topic: [api.get_message_type(msg)]},
                                 self.args.TOPIC, self.args.TYPE)
        if not common.filter_dict(dct, self.args.SKIP_TOPIC, self.args.SKIP_TYPE, reverse=True):
            return False
        if not super(AppSource, self).is_processable(topic, msg, stamp, index):
            return False
        if not ConditionMixin.is_processable(self, topic, msg, stamp, index):
            return False
        self._status = True
        return True

    def validate(self):
        """Returns whether configured arguments are valid, prints error if not."""
        if self.valid is not None: return self.valid
        self.valid = Source.validate(self)
        if self.valid:
            self._configure()
        return self.valid

    def _configure(self):
        """Adjusts start/end time filter values to current time."""
        if self.args.START_TIME is not None:
            self.args.START_TIME = api.make_live_time(self.args.START_TIME)
        if self.args.END_TIME is not None:
            self.args.END_TIME = api.make_live_time(self.args.END_TIME)


__all__ = ["AppSource", "ConditionMixin", "BagSource", "LiveSource", "Source"]

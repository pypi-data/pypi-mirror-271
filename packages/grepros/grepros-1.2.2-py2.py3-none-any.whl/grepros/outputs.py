# -*- coding: utf-8 -*-
"""
Main outputs for emitting messages.

------------------------------------------------------------------------------
This file is part of grepros - grep for ROS bag files and live topics.
Released under the BSD License.

@author      Erki Suurjaak
@created     23.10.2021
@modified    21.04.2024
------------------------------------------------------------------------------
"""
## @namespace grepros.outputs
from __future__ import print_function
import atexit
import collections
import datetime
import os
import re
import sys

import six
import yaml

from . import api
from . import common
from . common import ArgumentUtil, ConsolePrinter, MatchMarkers
from . inputs import Source


class Sink(object):
    """Output base class."""

    ## Auto-detection file extensions for subclasses, as (".ext", )
    FILE_EXTENSIONS = ()

    ## Constructor argument defaults
    DEFAULT_ARGS = dict(META=False)

    def __init__(self, args=None, **kwargs):
        """
        @param   args        arguments as namespace or dictionary, case-insensitive
        @param   args.meta   whether to emit metainfo
        @param   kwargs      any and all arguments as keyword overrides, case-insensitive
        """
        self._batch_meta = {}  # {source batch: "source metadata"}
        self._counts     = {}  # {(topic, typename, typehash): count}

        self.args = common.ensure_namespace(args, Sink.DEFAULT_ARGS, **kwargs)
        ## Result of validate()
        self.valid = None
        ## inputs.Source instance bound to this sink
        self.source = Source(self.args)

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Context manager exit, closes sink."""
        self.close()

    def emit_meta(self):
        """Outputs source metainfo like bag header as debug stream, if not already emitted."""
        batch = self.args.META and self.source.get_batch()
        if self.args.META and batch not in self._batch_meta:
            meta = self._batch_meta[batch] = self.source.format_meta()
            meta and ConsolePrinter.debug(meta)

    def emit(self, topic, msg, stamp=None, match=None, index=None):
        """
        Outputs ROS message.

        @param   topic  full name of ROS topic the message is from
        @param   msg    ROS message
        @param   stamp  message ROS timestamp, if not current ROS time
        @param   match  ROS message with values tagged with match markers if matched, else None
        @param   index  message index in topic, if any
        """
        topickey = api.TypeMeta.make(msg, topic).topickey
        self._counts[topickey] = self._counts.get(topickey, 0) + 1

    def bind(self, source):
        """Attaches source to sink."""
        self.source = source

    def configure(self, args=None, **kwargs):
        """
        Updates sink configuration.

        @param   args    arguments as namespace or dictionary, case-insensitive
        @param   kwargs  any and all arguments as keyword overrides, case-insensitive
        """
        self.args = common.ensure_namespace(args, vars(self.args), **kwargs)
        self.valid = None

    def validate(self):
        """Returns whether sink prerequisites are met (like ROS environment set if LiveSink)."""
        if self.valid is not None: return self.valid
        try: self.args, self.valid = ArgumentUtil.validate(self.args), True
        except Exception: self.valid = False
        return self.valid

    def close(self):
        """Shuts down output, closing any files or connections."""
        self._batch_meta.clear()
        self._counts.clear()

    def flush(self):
        """Writes out any pending data to disk."""

    def thread_excepthook(self, text, exc):
        """Handles exception, used by background threads."""
        ConsolePrinter.error(text)

    def is_highlighting(self):
        """Returns whether this sink requires highlighted matches."""
        return False

    @classmethod
    def autodetect(cls, target):
        """Returns true if target is recognizable as output for this sink class."""
        ext = os.path.splitext(target or "")[-1].lower()
        return ext in cls.FILE_EXTENSIONS

    def _ensure_stamp_index(self, topic, msg, stamp=None, index=None):
        """Returns (stamp, index) populated with current ROS time and topic index if `None`."""
        if stamp is None: stamp = api.get_rostime(fallback=True)
        if index is None: index = self._counts.get(api.TypeMeta.make(msg, topic).topickey, 0) + 1
        return stamp, index


class TextSinkMixin(object):
    """Provides message formatting as text."""

    ## Default highlight wrappers if not color output
    NOCOLOR_HIGHLIGHT_WRAPPERS = "**", "**"

    ## Constructor argument defaults
    DEFAULT_ARGS = dict(COLOR=True, EMIT_FIELD=(), NOEMIT_FIELD=(), HIGHLIGHT=True,
                        MAX_FIELD_LINES=None, START_LINE=None, END_LINE=None,
                        MAX_MESSAGE_LINES=None, LINES_AROUND_MATCH=None, MATCHED_FIELDS_ONLY=False,
                        WRAP_WIDTH=None, MATCH_WRAPPER=None)

    def __init__(self, args=None, **kwargs):
        """
        @param   args                       arguments as namespace or dictionary, case-insensitive
        @param   args.color                 False or "never" for not using colors in replacements
        @param   args.highlight             highlight matched values (default true)
        @param   args.emit_field            message fields to emit if not all
        @param   args.noemit_field          message fields to skip in output
        @param   args.max_field_lines       maximum number of lines to output per field
        @param   args.start_line            message line number to start output from
        @param   args.end_line              message line number to stop output at
        @param   args.max_message_lines     maximum number of lines to output per message
        @param   args.lines_around_match    number of message lines around matched fields to output
        @param   args.matched_fields_only   output only the fields where match was found
        @param   args.wrap_width            character width to wrap message YAML output at
        @param   args.match_wrapper         string to wrap around matched values,
                                            both sides if one value, start and end if more than one,
                                            or no wrapping if zero values
        @param   kwargs                     any and all arguments as keyword overrides, case-insensitive
        """
        self._prefix       = ""    # Put before each message line (filename if grepping 1+ files)
        self._wrapper      = None  # TextWrapper instance
        self._patterns     = {}    # {key: [(() if any field else ('path', ), re.Pattern), ]}
        self._format_repls = {}    # {text to replace if highlight: replacement text}
        self._styles = collections.defaultdict(str)  # {label: ANSI code string}


    def validate(self):
        """Returns whether arguments are valid, emits error if not, else populates options."""
        args = common.ensure_namespace(self.args, TextSinkMixin.DEFAULT_ARGS)
        try: args = ArgumentUtil.validate(args)
        except Exception: return False
        self._configure(args)
        return True


    def format_message(self, msg, highlight=False):
        """Returns message as formatted string, optionally highlighted for matches if configured."""
        if self.args.MAX_MESSAGE_LINES == 0: return ""
        text = self.message_to_yaml(msg).rstrip("\n")

        highlight = highlight and self.args.HIGHLIGHT
        if self._prefix or self.args.START_LINE or self.args.END_LINE \
        or self.args.MAX_MESSAGE_LINES or (self.args.LINES_AROUND_MATCH and highlight):
            lines = text.splitlines()

            if self.args.START_LINE or self.args.END_LINE or self.args.MAX_MESSAGE_LINES:
                start = self.args.START_LINE or 0
                start = max(start, -len(lines)) - (start > 0)  # <0 to sanity, >0 to 0-base
                end = self.args.END_LINE or len(lines)
                end = max(end, -len(lines)) - (end > 0)  # <0 to sanity, >0 to 0-base
                if self.args.MAX_MESSAGE_LINES: end = min(end, start + self.args.MAX_MESSAGE_LINES)
                lines = lines[start:end + 1]
                lines = lines and (lines[:-1] + [lines[-1] + self._styles["rst"]])

            if self.args.LINES_AROUND_MATCH and highlight:
                spans, NUM = [], self.args.LINES_AROUND_MATCH
                for i, l in enumerate(lines):
                    if MatchMarkers.START in l:
                        spans.append([max(0, i - NUM), min(i + NUM + 1, len(lines))])
                    if MatchMarkers.END in l and spans:
                        spans[-1][1] = min(i + NUM + 1, len(lines))
                lines = sum((lines[a:b - 1] + [lines[b - 1] + self._styles["rst"]]
                             for a, b in common.merge_spans(spans)), [])

            if self._prefix:
                lines = [self._prefix + l for l in lines]

            text = "\n".join(lines)

        for a, b in self._format_repls.items() if highlight else ():
            text = re.sub(r"(%s)\1+" % re.escape(a), r"\1", text)  # Remove consecutive duplicates
            text = text.replace(a, b)

        return text


    def message_to_yaml(self, val, top=(), typename=None):
        """Returns ROS message or other value as YAML."""
        # Refactored from genpy.message.strify_message().
        unquote = lambda v: v[1:-1] if v[:1] == v[-1:] == '"' else v

        def retag_match_lines(lines):
            """Adds match tags to lines where wrapping separated start and end."""
            PH = self._wrapper.placeholder
            for i, l in enumerate(lines):
                startpos0, endpos0 = l.find (MatchMarkers.START), l.find (MatchMarkers.END)
                startpos1, endpos1 = l.rfind(MatchMarkers.START), l.rfind(MatchMarkers.END)
                if endpos0 >= 0 and (startpos0 < 0 or startpos0 > endpos0):
                    lines[i] = l = re.sub(r"^(\s*)", r"\1" + MatchMarkers.START, l)
                if startpos1 >= 0 and endpos1 < startpos1 and i + 1 < len(lines):
                    lines[i + 1] = re.sub(r"^(\s*)", r"\1" + MatchMarkers.START, lines[i + 1])
                if startpos1 >= 0 and startpos1 > endpos1:
                    CUT, EXTRA = (-len(PH), PH) if PH and l.endswith(PH) else (len(l), "")
                    lines[i] = l[:CUT] + MatchMarkers.END + EXTRA
            return lines

        def truncate(v):
            """Returns text or list/tuple truncated to length used in final output."""
            if self.args.LINES_AROUND_MATCH \
            or (not self.args.MAX_MESSAGE_LINES and (self.args.END_LINE or 0) <= 0): return v

            MAX_CHAR_LEN = 1 + len(MatchMarkers.START) + len(MatchMarkers.END)
            # For list/tuple, account for comma and space
            if isinstance(v, (list, tuple)): textlen = bytelen = 2 + len(v) * (2 + MAX_CHAR_LEN)
            else: textlen, bytelen = self._wrapper.strlen(v), len(v)
            if textlen < 10000: return v

            # Heuristic optimization: shorten superlong texts before converting to YAML
            # if outputting a maximum number of lines per message
            # (e.g. a lidar pointcloud can be 10+MB of text and take 10+ seconds to format).
            MIN_CHARS_PER_LINE = self._wrapper.width
            if MAX_CHAR_LEN != 1:
                MIN_CHARS_PER_LINE = self._wrapper.width // MAX_CHAR_LEN * 2
            MAX_LINES = self.args.MAX_MESSAGE_LINES or self.args.END_LINE
            MAX_CHARS = MAX_LEN = MAX_LINES * MIN_CHARS_PER_LINE * self._wrapper.width + 100
            if bytelen > MAX_CHARS:  # Use worst-case max length plus some extra
                if isinstance(v, (list, tuple)): MAX_LEN = MAX_CHARS // 3
                v = v[:MAX_LEN]
            return v

        indent = "  " * len(top)
        if isinstance(val, six.integer_types + (float, bool)):
            return str(val)
        if isinstance(val, common.TEXT_TYPES):
            if val in ("", MatchMarkers.EMPTY):
                return MatchMarkers.EMPTY_REPL if val else "''"
            # default_style='"' avoids trailing "...\n"
            return yaml.safe_dump(truncate(val), default_style='"', width=sys.maxsize).rstrip("\n")
        if isinstance(val, (list, tuple)):
            if not val:
                return "[]"
            if api.scalar(typename) in api.ROS_STRING_TYPES:
                yaml_str = yaml.safe_dump(truncate(val)).rstrip('\n')
                return "\n" + "\n".join(indent + line for line in yaml_str.splitlines())
            vals = [x for i, v in enumerate(truncate(val))
                    for x in [self.message_to_yaml(v, top + (i, ), typename)] if x]
            if api.scalar(typename) in api.ROS_NUMERIC_TYPES:
                return "[%s]" % ", ".join(unquote(str(v)) for v in vals)
            return ("\n" + "\n".join(indent + "-   " + v for v in vals)) if vals else ""
        if api.is_ros_message(val):
            MATCHED_ONLY = self.args.MATCHED_FIELDS_ONLY and not self.args.LINES_AROUND_MATCH
            vals, fieldmap = [], api.get_message_fields(val)
            prints, noprints = self._patterns["print"], self._patterns["noprint"]
            fieldmap = api.filter_fields(fieldmap, top, include=prints, exclude=noprints)
            for k, t in fieldmap.items():
                v = self.message_to_yaml(api.get_message_value(val, k, t), top + (k, ), t)
                if not v or MATCHED_ONLY and MatchMarkers.START not in v:
                    continue  # for k, t

                if t not in api.ROS_STRING_TYPES: v = unquote(v)
                if api.scalar(t) in api.ROS_BUILTIN_TYPES:
                    is_strlist = t.endswith("]") and api.scalar(t) in api.ROS_STRING_TYPES
                    is_num = api.scalar(t) in api.ROS_NUMERIC_TYPES
                    extra_indent = indent if is_strlist else " " * len(indent + k + ": ")
                    self._wrapper.reserve_width(self._prefix + extra_indent)
                    self._wrapper.drop_whitespace = t.endswith("]") and not is_strlist
                    self._wrapper.break_long_words = not is_num
                    v = ("\n" + extra_indent).join(retag_match_lines(self._wrapper.wrap(v)))
                    if is_strlist and self._wrapper.strip(v) != "[]": v = "\n" + v
                vals.append("%s%s: %s" % (indent, k, api.format_message_value(val, k, v)))
            return ("\n" if indent and vals else "") + "\n".join(vals)

        return str(val)


    def _configure(self, args):
        """Initializes output settings."""
        self._patterns.clear()
        self._styles.clear()
        self._styles.default_factory = str
        prints, noprints = args.EMIT_FIELD, args.NOEMIT_FIELD
        for key, vals in [("print", prints), ("noprint", noprints)]:
            self._patterns[key] = [(tuple(v.split(".")), common.path_to_regex(v)) for v in vals]

        if args.COLOR not in ("never", False):
            self._styles.update({"hl0":  ConsolePrinter.STYLE_HIGHLIGHT if self.args.HIGHLIGHT
                                         else "",
                                 "ll0":  ConsolePrinter.STYLE_LOWLIGHT,
                                 "pfx0": ConsolePrinter.STYLE_SPECIAL,  # Content line prefix start
                                 "sep0": ConsolePrinter.STYLE_SPECIAL2})
            self._styles.default_factory = lambda: ConsolePrinter.STYLE_RESET

        WRAPS = args.MATCH_WRAPPER if self.args.HIGHLIGHT else ""
        if WRAPS is None and args.COLOR in ("never", False): WRAPS = self.NOCOLOR_HIGHLIGHT_WRAPPERS
        WRAPS = ((WRAPS or [""]) * 2)[:2]
        self._styles["hl0"] = self._styles["hl0"] + WRAPS[0]
        self._styles["hl1"] = WRAPS[1] + self._styles["hl1"]

        custom_widths = {MatchMarkers.START: len(WRAPS[0]), MatchMarkers.END:     len(WRAPS[1]),
                         self._styles["ll0"]:            0, self._styles["ll1"]:  0,
                         self._styles["pfx0"]:           0, self._styles["pfx1"]: 0,
                         self._styles["sep0"]:           0, self._styles["sep1"]: 0}
        wrapargs = dict(max_lines=args.MAX_FIELD_LINES,
                        placeholder="%s ...%s" % (self._styles["ll0"], self._styles["ll1"]))
        if args.WRAP_WIDTH is not None: wrapargs.update(width=args.WRAP_WIDTH)
        self._wrapper = common.TextWrapper(custom_widths=custom_widths, **wrapargs)
        self._format_repls = {MatchMarkers.START: self._styles["hl0"],
                              MatchMarkers.END:   self._styles["hl1"]}



class RolloverSinkMixin(object):
    """Provides output file rollover by size, duration, or message count."""

    ## Constructor argument defaults
    DEFAULT_ARGS = dict(WRITE=None, WRITE_OPTIONS={}, VERBOSE=False)

    ## Command-line help templates for rollover options, as [(name, text with %s label placeholder)]
    OPTIONS_TEMPLATES = [
        ("rollover-size=NUM",           "size limit for individual files\nin {label} output\n"
                                        "as bytes (supports abbreviations like 1K or 2M or 3G)"),
        ("rollover-count=NUM",          "message limit for individual files\nin {label} output\n"
                                        "(supports abbreviations like 1K or 2M or 3G)"),
        ("rollover-duration=INTERVAL",  "message time span limit for individual files\n"
                                        "in {label} output\n"
                                        "as seconds (supports abbreviations like 60m or 2h or 1d)"),
        ("rollover-template=STR",       "output filename template for individual files\n"
                                        "in {label} output,\n"
                                        'supporting strftime format codes like "%%H-%%M-%%S"\n'
                                        'and "%%(index)s" as output file index'),
    ]

    START_META_TEMPLATE = "{mcount} in {tcount} to "

    FILE_META_TEMPLATE = "{name} ({size})"

    MULTI_META_TEMPLATE = "\n- {name} ({size}, {mcount}, {tcount})"


    def __init__(self, args=None, **kwargs):
        """
        @param   args                 arguments as namespace or dictionary, case-insensitive
        @param   args.write           base name of output file to write if not using rollover-template
        @param   args.write_options   {"rollover-size": bytes limit for individual output files,
                                       "rollover-count": message limit for individual output files,
                                       "rollover-duration": time span limit for individual output files,
                                                            as ROS duration or convertible seconds,
                                       "rollover-template": output filename template, supporting
                                                            strftime format codes like "%H-%M-%S"
                                                            and "%(index)s" as output file index,
                                       "overwrite": whether to overwrite existing file
                                                    (default false)}
        @param   args.verbose         whether to emit debug information
        @param   kwargs               any and all arguments as keyword overrides, case-insensitive
        """
        self._rollover_limits = {}  # {?"size": int, ?"count": int, ?"duration": ROS duration}
        self._rollover_template = None
        self._rollover_files = collections.OrderedDict()  # {path: {"counts", "start", "size"}}

        ## Current output file path
        self.filename = None


    def validate(self):
        """Returns whether write options are valid, emits error if not, else populates options."""
        ok = True
        self._rollover_limits.clear()
        self._rollover_template = None
        for k in ("size", "count", "duration"):
            value = value0 = self.args.WRITE_OPTIONS.get("rollover-%s" % k)
            if value is None: continue  # for k
            SUFFIXES = dict(zip("smhd", [1, 60, 3600, 24*3600])) if "duration" == k else \
                       dict(zip("KMGT", [2**10, 2**20, 2**30, 2**40])) if "size" == k else \
                       dict(zip("KMGT", [10**3, 10**6, 10**9, 10**12]))
            try:
                if isinstance(value, (six.binary_type, six.text_type)):
                    value = common.parse_number(value, SUFFIXES)
                value = (api.to_duration if "duration" == k else int)(value)
            except Exception: pass
            if (value is None or value < 0) if "duration" != k \
            else (k != api.get_ros_time_category(value) or api.to_sec(value) < 0):
                ConsolePrinter.error("Invalid rollover %s option: %r. "
                                     "Value must be a non-negative %s.", k, value0, k)
                ok = False
            elif value:
                self._rollover_limits[k] = value
        if self.args.WRITE_OPTIONS.get("rollover-template"):
            value = self.args.WRITE_OPTIONS["rollover-template"]
            value = re.sub(r"(^|[^%])%\(index\)", r"\1%%(index)", value)
            try: datetime.datetime.now().strftime(value)
            except Exception:
                ConsolePrinter.error("Invalid rollover template option: %r. "
                                     "Value must contain valid strftime codes.", value)
                ok = False
            else:
                if ok:
                    self._rollover_template = value
                if ok and not self._rollover_limits:
                    ConsolePrinter.warn("Ignoring rollover template option: "
                                        "no rollover limits given.")
        return ok


    def ensure_rollover(self, topic, msg, stamp):
        """
        Closes current output file and prepares new filename if rollover limit reached.
        """
        if not self._rollover_limits: return

        self.filename = self.filename or self.make_filename()
        do_rollover, props = False, self._rollover_files.setdefault(self.filename, {})
        stamp = api.time_message(stamp, to_message=False)  # Ensure rclpy stamp in ROS2

        if self._rollover_limits.get("size") and props:
            props["size"] = self.size
            do_rollover = (props["size"] or 0) >= self._rollover_limits["size"]
        if not do_rollover and self._rollover_limits.get("count") and props:
            do_rollover = (sum(props["counts"].values()) >= self._rollover_limits["count"])
        if not do_rollover and self._rollover_limits.get("duration") and props:
            stamps = [stamp, props["start"]]
            do_rollover = (max(stamps) - min(stamps) >= self._rollover_limits["duration"])
        if do_rollover:
            self.close_output()
            props["size"] = self.size
            self.filename = self.make_filename()
            props = self._rollover_files[self.filename] = {}

        topickey = api.TypeMeta.make(msg, topic).topickey
        if not props: props.update({"counts": {}, "start": stamp, "size": None})
        props["start"] = min((props["start"], stamp))
        props["counts"][topickey] = props["counts"].get(topickey, 0) + 1


    def close_output(self):
        """Closes output file, if any."""
        raise NotImplementedError


    def make_filename(self):
        """Returns new filename for output, accounting for rollover template and overwrite."""
        result = self.args.WRITE
        if self._rollover_template and self._rollover_limits:
            result = datetime.datetime.now().strftime(self._rollover_template)
            try: result %= {"index": len(self._rollover_files)}
            except Exception: pass
        if self.args.WRITE_OPTIONS.get("overwrite") not in (True, "true"):
            result = common.unique_path(result, empty_ok=True)
        return result


    def format_output_meta(self):
        """Returns output file metainfo string, with names and sizes and message/topic counts."""
        if not self._counts: return ""
        SIZE_ERROR = "error getting size"
        result = self.START_META_TEMPLATE.format(
            mcount=common.plural("message", sum(self._counts.values())),
            tcount=common.plural("topic", self._counts)
        )
        if len(self._rollover_files) < 2:
            sz = self.size
            sizestr = SIZE_ERROR if sz is None else common.format_bytes(sz)
            result += self.FILE_META_TEMPLATE.format(name=self.filename, size=sizestr) + "."
        else:
            for path, props in self._rollover_files.items():
                if props["size"] is None:
                    try: props["size"] = os.path.getsize(path)
                    except Exception as e:
                        ConsolePrinter.warn("Error getting size of %s: %s", path, e)
            sizesum = sum(x["size"] for x in self._rollover_files.values() if x["size"] is not None)
            result += self.FILE_META_TEMPLATE.format(
                name=common.plural("file", self._rollover_files),
                size=common.format_bytes(sizesum)
            ) + (":" if self.args.VERBOSE else ".")
            for path, props in self._rollover_files.items() if self.args.VERBOSE else ():
                sizestr = SIZE_ERROR if props["size"] is None else common.format_bytes(props["size"])
                result += self.MULTI_META_TEMPLATE.format(name=path, size=sizestr,
                    mcount=common.plural("message", sum(props["counts"].values())),
                    tcount=common.plural("topic", props["counts"])
                )
        return result


    @property
    def size(self):
        """Returns current file size in bytes, or None if size lookup failed."""
        try: return os.path.getsize(self.filename)
        except Exception as e:
            ConsolePrinter.warn("Error getting size of %s: %s", self.filename, e)
            return None


    @classmethod
    def get_write_options(cls, label):
        """Returns command-line help texts for rollover options, as [(name, help)]."""
        return [(k, v.format(label=label)) for k, v in cls.OPTIONS_TEMPLATES]



class ConsoleSink(Sink, TextSinkMixin):
    """Prints messages to console."""

    META_LINE_TEMPLATE   = "{ll0}{sep} {line}{ll1}"
    MESSAGE_SEP_TEMPLATE = "{ll0}{sep}{ll1}"
    PREFIX_TEMPLATE      = "{pfx0}{batch}{pfx1}{sep0}{sep}{sep1}"
    MATCH_PREFIX_SEP     = ":"    # Printed after bag filename for matched message lines
    CONTEXT_PREFIX_SEP   = "-"    # Printed after bag filename for context message lines
    SEP                  = "---"  # Prefix of message separators and metainfo lines

    ## Constructor argument defaults
    DEFAULT_ARGS = dict(COLOR=True, EMIT_FIELD=(), NOEMIT_FIELD=(), HIGHLIGHT=True, META=False,
                        LINE_PREFIX=True, MAX_FIELD_LINES=None, START_LINE=None,
                        END_LINE=None, MAX_MESSAGE_LINES=None, LINES_AROUND_MATCH=None,
                        MATCHED_FIELDS_ONLY=False, WRAP_WIDTH=None, MATCH_WRAPPER=None)


    def __init__(self, args=None, **kwargs):
        """
        @param   args                       arguments as namespace or dictionary, case-insensitive
        @param   args.color                 False or "never" for not using colors in replacements
        @param   args.highlight             highlight matched values (default true)
        @param   args.meta                  whether to print metainfo
        @param   args.emit_field            message fields to emit if not all
        @param   args.noemit_field          message fields to skip in output
        @param   args.line_prefix           print source prefix like bag filename on each message line
        @param   args.max_field_lines       maximum number of lines to print per field
        @param   args.start_line            message line number to start output from
        @param   args.end_line              message line number to stop output at
        @param   args.max_message_lines     maximum number of lines to output per message
        @param   args.lines_around_match    number of message lines around matched fields to output
        @param   args.matched_fields_only   output only the fields where match was found
        @param   args.wrap_width            character width to wrap message YAML output at
        @param   args.match_wrapper         string to wrap around matched values,
                                            both sides if one value, start and end if more than one,
                                            or no wrapping if zero values
        @param   kwargs                     any and all arguments as keyword overrides, case-insensitive
        """
        args = common.ensure_namespace(args, ConsoleSink.DEFAULT_ARGS, **kwargs)
        super(ConsoleSink, self).__init__(args)
        TextSinkMixin.__init__(self, args)


    def emit_meta(self):
        """Prints source metainfo like bag header, if not already printed."""
        if not self.validate(): raise Exception("invalid")
        batch = self.args.META and self.source.get_batch()
        if self.args.META and batch not in self._batch_meta:
            meta = self._batch_meta[batch] = self.source.format_meta()
            kws = dict(self._styles, sep=self.SEP)
            meta = "\n".join(x and self.META_LINE_TEMPLATE.format(**dict(kws, line=x))
                             for x in meta.splitlines())
            meta and ConsolePrinter.print(meta)


    def emit(self, topic, msg, stamp=None, match=None, index=None):
        """Prints separator line and message text."""
        if not self.validate(): raise Exception("invalid")
        self._prefix = ""
        stamp, index = self._ensure_stamp_index(topic, msg, stamp, index)
        if self.args.LINE_PREFIX and self.source.get_batch():
            sep = self.MATCH_PREFIX_SEP if match else self.CONTEXT_PREFIX_SEP
            kws = dict(self._styles, sep=sep, batch=self.source.get_batch())
            self._prefix = self.PREFIX_TEMPLATE.format(**kws)
        kws = dict(self._styles, sep=self.SEP)
        if self.args.META:
            meta = self.source.format_message_meta(topic, msg, stamp, index)
            meta = "\n".join(x and self.META_LINE_TEMPLATE.format(**dict(kws, line=x))
                             for x in meta.splitlines())
            meta and ConsolePrinter.print(meta)
        elif self._counts:
            sep = self.MESSAGE_SEP_TEMPLATE.format(**kws)
            sep and ConsolePrinter.print(sep)
        ConsolePrinter.print(self.format_message(match or msg, highlight=bool(match)))
        super(ConsoleSink, self).emit(topic, msg, stamp, match, index)


    def is_highlighting(self):
        """Returns True if sink is configured to highlight matched values."""
        return bool(self.args.HIGHLIGHT)


    def validate(self):
        """Returns whether arguments environment set, populates options, emits error if not."""
        if self.valid is not None: return self.valid
        if self.args.WRAP_WIDTH is None:
            self.args.WRAP_WIDTH = ConsolePrinter.WIDTH
        self.valid = Sink.validate(self) and TextSinkMixin.validate(self)
        return self.valid



class BagSink(Sink, RolloverSinkMixin):
    """Writes messages to bagfile."""

    ## Constructor argument defaults
    DEFAULT_ARGS = dict(META=False, WRITE_OPTIONS={}, VERBOSE=False)

    def __init__(self, args=None, **kwargs):
        """
        @param   args                 arguments as namespace or dictionary, case-insensitive;
                                      or a single path as the ROS bagfile to write,
                                      or a stream or {@link grepros.api.Bag Bag} instance to write to
        @param   args.write           name of ROS bagfile to create or append to,
                                      or a stream to write to
        @param   args.write_options   {"overwrite": whether to overwrite existing file
                                                    (default false),
                                       "rollover-size": bytes limit for individual output files,
                                       "rollover-count": message limit for individual output files,
                                       "rollover-duration": time span limit for individual output files,
                                                            as ROS duration or convertible seconds,
                                       "rollover-template": output filename template, supporting
                                                            strftime format codes like "%H-%M-%S"
                                                            and "%(index)s" as output file index}
        @param   args.meta            whether to emit metainfo
        @param   args.verbose         whether to emit debug information
        @param   kwargs               any and all arguments as keyword overrides, case-insensitive
        """

        args0 = args
        args = {"WRITE": str(args)} if isinstance(args, common.PATH_TYPES) else \
               {"WRITE": args} if common.is_stream(args) else \
               {} if isinstance(args, api.Bag) else args
        args = common.ensure_namespace(args, BagSink.DEFAULT_ARGS, **kwargs)
        super(BagSink, self).__init__(args)
        RolloverSinkMixin.__init__(self, args)
        self._bag = args0 if isinstance(args0, api.Bag) else None
        self._overwrite = (args.WRITE_OPTIONS.get("overwrite") in ("true", True))
        self._close_printed = False
        self._is_pathed = self._bag is None and not common.is_stream(self.args.WRITE)

        atexit.register(self.close)

    def emit(self, topic, msg, stamp=None, match=None, index=None):
        """Writes message to output bagfile."""
        if not self.validate(): raise Exception("invalid")
        stamp, index = self._ensure_stamp_index(topic, msg, stamp, index)
        if self._is_pathed: RolloverSinkMixin.ensure_rollover(self, topic, msg, stamp)
        self._ensure_open()
        topickey = api.TypeMeta.make(msg, topic).topickey
        if self.args.VERBOSE and topickey not in self._counts:
            ConsolePrinter.debug("Adding topic %s in bag output.", topic)

        qoses = self.source.get_message_meta(topic, msg, stamp).get("qoses")
        self._bag.write(topic, msg, stamp, qoses=qoses)
        super(BagSink, self).emit(topic, msg, stamp, match, index)

    def validate(self):
        """Returns whether write options are valid and ROS environment set, emits error if not."""
        if self.valid is not None: return self.valid
        result = Sink.validate(self)
        if not RolloverSinkMixin.validate(self):
            result = False
        if self.args.WRITE_OPTIONS.get("overwrite") not in (None, True, False, "true", "false"):
            ConsolePrinter.error("Invalid overwrite option for bag: %r. "
                                 "Choose one of {true, false}.",
                                 self.args.WRITE_OPTIONS["overwrite"])
            result = False
        if not self._bag \
        and not common.verify_io(self.make_filename() if self._is_pathed else self.args.WRITE, "w"):
            ConsolePrinter.error("File not writable.")
            result = False
        if not self._bag and common.is_stream(self.args.WRITE) \
        and not any(c.STREAMABLE for c in api.Bag.WRITER_CLASSES):
            ConsolePrinter.error("Bag format does not support writing streams.")
            result = False
        if self._bag and self._bag.mode not in ("a", "w"):
            ConsolePrinter.error("Bag not in write mode.")
            result = False
        self.valid = api.validate() and result
        return self.valid

    def close(self):
        """Closes output bag, if any, emits metainfo."""
        self._bag and self._bag.close()
        if not self._close_printed and self._counts and self._bag:
            self._close_printed = True
            ConsolePrinter.debug("Wrote bag output for %s", self.format_output_meta())
        super(BagSink, self).close()

    def close_output(self):
        """Closes output bag, if any."""
        self._bag and self._bag.close()
        self._bag = None

    @property
    def size(self):
        """Returns current file size in bytes, or None if size lookup failed."""
        try: return os.path.getsize(self._bag.filename if self._bag else self.filename) \
                    if not self._bag or (self._bag.filename and api.ROS1) else self._bag.size
        except Exception as e:
            ConsolePrinter.warn("Error getting size of %s: %s", self.filename, e)
            return None

    def _ensure_open(self):
        """Opens output file if not already open."""
        if self._bag is not None:
            if self._bag.closed:
                self._bag.open()
                self._close_printed = False
            return
        self._close_printed = False
        if common.is_stream(self.args.WRITE):
            self._bag = api.Bag(self.args.WRITE, mode=getattr(self.args.WRITE, "mode", "w"))
            self.filename = "<stream>"
            return

        filename = self.filename = self.filename or self.make_filename()
        if not self._overwrite and os.path.isfile(filename) and os.path.getsize(filename):
            cls = api.Bag.autodetect(filename)
            if cls and "a" not in getattr(cls, "MODES", ("a", )):
                filename = self.filename = common.unique_path(filename)
                if self.args.VERBOSE:
                    ConsolePrinter.debug("Making unique filename %r, as %s does not support "
                                         "appending.", filename, cls.__name___)
        if self.args.VERBOSE:
            sz = os.path.isfile(filename) and os.path.getsize(filename)
            ConsolePrinter.debug("%s bag output %s%s.",
                                 "Overwriting" if sz and self._overwrite else
                                 "Appending to" if sz else "Creating",
                                 filename, (" (%s)" % common.format_bytes(sz)) if sz else "")
        common.makedirs(os.path.dirname(filename))
        self._bag = api.Bag(filename, mode="w" if self._overwrite else "a")

    @classmethod
    def autodetect(cls, target):
        """Returns true if target is recognizable as a ROS bag."""
        ext = os.path.splitext(target or "")[-1].lower()
        return ext in api.BAG_EXTENSIONS


class LiveSink(Sink):
    """Publishes messages to ROS topics."""

    ## Constructor argument defaults
    DEFAULT_ARGS = dict(LIVE=False, META=False, QUEUE_SIZE_OUT=10, PUBLISH_PREFIX="",
                        PUBLISH_SUFFIX="", PUBLISH_FIXNAME="", VERBOSE=False)

    def __init__(self, args=None, **kwargs):
        """
        @param   args                   arguments as namespace or dictionary, case-insensitive
        @param   args.live              whether reading messages from live ROS topics
        @param   args.queue_size_out    publisher queue size (default 10)
        @param   args.publish_prefix    output topic prefix, prepended to input topic
        @param   args.publish_suffix    output topic suffix, appended to output topic
        @param   args.publish_fixname   single output topic name to publish to,
                                        overrides prefix and suffix if given
        @param   args.meta              whether to emit metainfo
        @param   args.verbose           whether to emit debug information
        @param   kwargs                 any and all arguments as keyword overrides, case-insensitive
        """
        args = common.ensure_namespace(args, LiveSink.DEFAULT_ARGS, **kwargs)
        super(LiveSink, self).__init__(args)
        self._pubs = {}  # {(intopic, typename, typehash): ROS publisher}
        self._close_printed = False

    def emit(self, topic, msg, stamp=None, match=None, index=None):
        """Publishes message to output topic."""
        if not self.validate(): raise Exception("invalid")
        api.init_node()
        with api.TypeMeta.make(msg, topic) as m:
            topickey, cls = (m.topickey, m.typeclass)
        if topickey not in self._pubs:
            topic2 = self.args.PUBLISH_PREFIX + topic + self.args.PUBLISH_SUFFIX
            topic2 = self.args.PUBLISH_FIXNAME or topic2
            if self.args.VERBOSE:
                ConsolePrinter.debug("Publishing from %s to %s.", topic, topic2)

            pub = None
            if self.args.PUBLISH_FIXNAME:
                pub = next((v for (_, c), v in self._pubs.items() if c == cls), None)
            pub = pub or api.create_publisher(topic2, cls, queue_size=self.args.QUEUE_SIZE_OUT)
            self._pubs[topickey] = pub

        self._pubs[topickey].publish(msg)
        self._close_printed = False
        super(LiveSink, self).emit(topic, msg, stamp, match, index)

    def bind(self, source):
        """Attaches source to sink and blocks until connected to ROS."""
        if not self.validate(): raise Exception("invalid")
        super(LiveSink, self).bind(source)
        api.init_node()

    def validate(self):
        """
        Returns whether ROS environment is set for publishing,
        and output topic configuration is valid, emits error if not.
        """
        if self.valid is not None: return self.valid
        result = Sink.validate(self)
        if not api.validate(live=True):
            result = False
        config_ok = True
        if self.args.LIVE and not any((self.args.PUBLISH_PREFIX, self.args.PUBLISH_SUFFIX,
                                       self.args.PUBLISH_FIXNAME)):
            ConsolePrinter.error("Need topic prefix or suffix or fixname "
                                 "when republishing messages from live ROS topics.")
            config_ok = False
        self.valid = result and config_ok
        return self.valid

    def close(self):
        """Shuts down publishers."""
        if not self._close_printed and self._counts:
            self._close_printed = True
            ConsolePrinter.debug("Published %s to %s.",
                                 common.plural("message", sum(self._counts.values())),
                                 common.plural("topic", self._pubs))
        for k in list(self._pubs):
            try: self._pubs.pop(k).unregister()
            except Exception as e:
                if self.args.VERBOSE:
                    ConsolePrinter.warn("Error closing publisher on topic %r: %s", k[0], e)
        super(LiveSink, self).close()


class AppSink(Sink):
    """Provides messages to callback function."""

    ## Constructor argument defaults
    DEFAULT_ARGS = dict(EMIT=None, METAEMIT=None, HIGHLIGHT=False)

    def __init__(self, args=None, **kwargs):
        """
        @param   args             arguments as namespace or dictionary, case-insensitive;
                                  or emit callback
        @param   args.emit        callback(topic, msg, stamp, highlighted msg, index in topic), if any
        @param   args.metaemit    callback(metadata dict) if any, invoked before first emit from source batch
        @param   args.highlight   whether to expect highlighted matching fields from source messages
        @param   kwargs           any and all arguments as keyword overrides, case-insensitive
        """
        if callable(args): args = common.ensure_namespace(None, emit=args)
        args = common.ensure_namespace(args, AppSink.DEFAULT_ARGS, **kwargs)
        super(AppSink, self).__init__(args)

    def emit_meta(self):
        """Invokes registered metaemit callback, if any, and not already invoked."""
        if not self.validate(): raise Exception("invalid")
        if not self.source: return
        batch = self.source.get_batch() if self.args.METAEMIT else None
        if self.args.METAEMIT and batch not in self._batch_meta:
            meta = self._batch_meta[batch] = self.source.get_meta()
            self.args.METAEMIT(meta)

    def emit(self, topic, msg, stamp=None, match=None, index=None):
        """Registers message and invokes registered emit callback, if any."""
        if not self.validate(): raise Exception("invalid")
        stamp, index = self._ensure_stamp_index(topic, msg, stamp, index)
        super(AppSink, self).emit(topic, msg, stamp, match, index)
        if self.args.EMIT: self.args.EMIT(topic, msg, stamp, match, index)

    def is_highlighting(self):
        """Returns whether emitted matches are highlighted."""
        return self.args.HIGHLIGHT

    def validate(self):
        """Returns whether callbacks are valid, emits error if not."""
        if self.valid is not None: return self.valid
        self.valid = True
        for key in ("EMIT", "METAEMIT"):
            if getattr(self.args, key) and not callable(getattr(self.args, key)):
                ConsolePrinter.error("Invalid callback for %s: %r", key, getattr(self.args, key))
                self.valid = False
        return self.valid


class MultiSink(Sink):
    """Combines any number of sinks."""

    ## Autobinding between argument flags and sink classes
    FLAG_CLASSES = {"PUBLISH": LiveSink, "CONSOLE": ConsoleSink, "APP": AppSink}

    ## Autobinding between `--write TARGET format=FORMAT` and sink classes
    FORMAT_CLASSES = {"bag": BagSink}

    def __init__(self, args=None, sinks=(), **kwargs):
        """
        Accepts more arguments, given to the real sinks constructed.

        @param   args           arguments as namespace or dictionary, case-insensitive
        @param   args.console   print matches to console
        @param   args.write     [[target, format=FORMAT, key=value, ], ]
        @param   args.publish   publish matches to live topics
        @param   args.app       provide messages to given callback function
        @param   sinks          pre-created sinks, arguments will be ignored
        @param   kwargs         any and all arguments as keyword overrides, case-insensitive
        """
        args = common.ensure_namespace(args, **kwargs)
        super(MultiSink, self).__init__(args)
        self.valid = True

        ## List of all combined sinks
        self.sinks = [cls(args) for flag, cls in self.FLAG_CLASSES.items()
                      if getattr(args, flag, None)] if not sinks else list(sinks)

        for dumpopts in getattr(args, "WRITE", []) if not sinks else ():
            kwargs = dict(x.split("=", 1) for x in dumpopts[1:] if isinstance(x, common.TEXT_TYPES))
            kwargs.update(kv for x in dumpopts[1:] if isinstance(x, dict) for kv in x.items())
            target, cls = dumpopts[0], self.FORMAT_CLASSES.get(kwargs.pop("format", None))
            if not cls:
                cls = next((c for c in sorted(self.FORMAT_CLASSES.values(),
                                              key=lambda x: x is BagSink)
                            if callable(getattr(c, "autodetect", None))
                            and c.autodetect(target)), None)
            if not cls:
                ConsolePrinter.error('Unknown output format in "%s"' % " ".join(map(str, dumpopts)))
                self.valid = False
                continue  # for dumpopts
            clsargs = common.structcopy(args)
            clsargs.WRITE, clsargs.WRITE_OPTIONS = target, kwargs
            self.sinks += [cls(clsargs)]

    def emit_meta(self):
        """Outputs source metainfo in one sink, if not already emitted."""
        if not self.validate(): raise Exception("invalid")
        sink = next((s for s in self.sinks if isinstance(s, ConsoleSink)), None)
        # Emit meta in one sink only, prefer console
        sink = sink or self.sinks[0] if self.sinks else None
        sink and sink.emit_meta()

    def emit(self, topic, msg, stamp=None, match=None, index=None):
        """Outputs ROS message to all sinks."""
        if not self.validate(): raise Exception("invalid")
        stamp, index = self._ensure_stamp_index(topic, msg, stamp, index)
        for sink in self.sinks:
            sink.emit(topic, msg, stamp, match, index)
        super(MultiSink, self).emit(topic, msg, stamp, match, index)

    def bind(self, source):
        """Attaches source to all sinks, sets thread_excepthook on all sinks."""
        super(MultiSink, self).bind(source)
        for sink in self.sinks:
            sink.bind(source)
            sink.thread_excepthook = self.thread_excepthook

    def configure(self, args=None, **kwargs):
        """
        Updates sinks configuration.

        @param   args    arguments as namespace or dictionary, case-insensitive
        @param   kwargs  any and all arguments as keyword overrides, case-insensitive
        """
        args = common.ensure_namespace(args, **kwargs)
        hasattr(args, "WRITE") and delattr(args, "WRITE")  # Special arg for MultiSink
        for sink in self.sinks: sink.configure(args, **kwargs)

    def validate(self):
        """Returns whether prerequisites are met for all sinks."""
        if not self.sinks:
            ConsolePrinter.error("No output configured.")
        return bool(self.sinks) and all([sink.validate() for sink in self.sinks]) and self.valid

    def close(self):
        """Closes all sinks."""
        for sink in self.sinks:
            sink.close()

    def flush(self):
        """Flushes all sinks."""
        for sink in self.sinks:
            sink.flush()

    def is_highlighting(self):
        """Returns whether any sink requires highlighted matches."""
        return any(s.is_highlighting() for s in self.sinks)


__all__ = [
    "AppSink", "BagSink", "ConsoleSink", "LiveSink", "MultiSink", "RolloverSinkMixin", "Sink",
    "TextSinkMixin",
]

import re
import logging
from typing import Literal, Optional, Dict, Callable

from .default import (_ansi_colors,
                      _ansi_styles,
                      _ansi_reset_all,
                      _default_custom_tags)


def wrap_dict(d: dict):
    class WrappedDict:
        pass

    wrapped = WrappedDict()
    for k, v in d.items():
        setattr(wrapped, k, v)
    return wrapped


class ExtFormatter(logging.Formatter):
    """
    Styling logs by tags with HTML-like syntax.
    """
    def __init__(
        self,
        fmt: Optional[str] = "%(message)s",
        datefmt: Optional[str] = "%(asctime)s",
        style: Literal["%", "{", "$"] = "%",
        excfmt: Optional[str] = "%(exc)s",
        stackfmt: Optional[str] = "%(stack)s",
        custom_tags: Optional[Dict[str, Callable[[logging.LogRecord], str]]] = {}
    ):
        """
        Parameters
        ----------
        fmt : Optional[str] = "%(message)s"
            String with message formatting template.
        datefmt : Optional[str] = "%(asctime)s"
            String with datetime formatting template.
        style : Literal["%", "{", "$"] = "%"
            Type of formatting.
        excfmt : Optional[str] = "%(exc)s"
            String with exception formatting template.
        stackfmt : Optional[str] = "%(stack)s"
            String with stack formatting template.
        custom_tags: Optional[Dict[str, Callable[[logging.LogRecord], str]]] = {}
            Dict of custom tags for formatting. 

        Example
        -------
        >>> formatter = extlog.ExtFormatter(
                fmt="<br-black>%(asctime)s</> [<level>%(levelname)s</>] <i><br-black>%(name)s</> <lvlmsg>%(message)s</>",
                datefmt="%Y-%m-%d %H:%M:%S",
                excfmt="<red>%(exc)s</>",
                stackfmt="<i><br-black>%(stack)s</>"
                custom_tags={
                    "level": lambda record: levels.get(record.levelno),
                }
            )
        """

        self.style = style

        self._ansi_colors = _ansi_colors
        self._ansi_styles = _ansi_styles
        self._ansi_reset_all = _ansi_reset_all

        logging._STYLES[style][0](excfmt).validate()
        logging._STYLES[style][0](stackfmt).validate()

        self.excfmt = excfmt
        self.stackfmt = stackfmt

        self.custom_tags = _default_custom_tags | custom_tags
        
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def _tag_as_ansi(self, tag: str, record: logging.LogRecord = None):
        """
        Converting tag to ANSI format.
        
        Parameters
        ----------
        tag : str
            HTML-like tag of style.
        record : logging.LogRecord = None
            LogRecord object. Required to working with custom tags.

        Returns
        -------
        str
            Tag as ANSI.

        Raises
        ------
        AttributeError
            LogRecord must be specified for use a custom tags.
        """
        if tag == "</>":
            return self._ansi_reset_all
        
        tag_name = tag.replace("<", "").replace(">", "")

        if tag_name.replace("bg-", "") in self._ansi_colors.keys():
            offset = 0
            if tag_name.startswith("bg-"):
                offset = 10
                tag_name = tag_name.replace("bg-", "")
            return f"\033[{self._ansi_colors[tag_name] + offset}m"
        elif tag_name in self._ansi_styles.keys():
            return f"\033[{self._ansi_styles[tag_name]}m"
        elif tag_name in self.custom_tags.keys():
            if record is None:
                raise AttributeError("LogRecord must be specified for use a custom tags")
            out = self.custom_tags[tag_name](record)
            for tag in self._find_tags(out):
                out = out.replace(tag, self._tag_as_ansi(tag, record))
            return out
        else:
            return tag
    
    def _find_tags(self, text: str):
        tag_pattern = re.compile(r'<[^>]+>')
        tags = tag_pattern.findall(text)
        return list(set(tags))

    def formatMessage(self, record: logging.LogRecord) -> str:
        message = super().formatMessage(record)
        tags = self._find_tags(message)
        for tag in tags:
            message = message.replace(tag, self._tag_as_ansi(tag, record))
        return message
    
    def formatException(self, record: logging.LogRecord):
        ei = record.exc_info
        exc = super().formatException(ei)
        exc = logging._STYLES[self.style][0](self.excfmt).format(wrap_dict({"exc": exc}))
        tags = self._find_tags(exc)
        for tag in tags:
            exc = exc.replace(tag, self._tag_as_ansi(tag, record))
        return exc
    
    def formatStack(self, record: logging.LogRecord):
        stack_info = record.stack_info
        stack = super().formatStack(stack_info)
        stack = logging._STYLES[self.style][0](self.stackfmt).format(wrap_dict({"stack": stack}))
        tags = self._find_tags(stack)
        for tag in tags:
            stack = stack.replace(tag, self._tag_as_ansi(tag, record))
        return stack

    def format(self, record):
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        s = self.formatMessage(record)
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(record)
        return s

import logging
from typing import Dict, Callable


TRACE = 5
SUCCESS = 25

logging.TRACE = TRACE
logging.SUCCESS = SUCCESS


_ansi_colors = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,

# bright colors
    "br-black": 90,
    "br-red": 91,
    "br-green": 92,
    "br-yellow": 93,
    "br-blue": 94,
    "br-magenta": 95,
    "br-cyan": 96,
    "br-white": 97,
}

# Also you can use prefix "bg-" for override color tag to background. 
# Example like "bg-green".

_ansi_styles = {
    "b": 1,
    "bold": 1,
    "d": 2,
    "dim": 2,
    "u": 4,
    "underline": 4,
    "o": 53,
    "overline": 53,
    "i": 3,
    "italic": 3,
    "r": 7,
    "reverse": 7,
    "s": 9,
    "striked": 9
}

_ansi_reset_all = "\033[0m"

# default values
_default_level_mod = {
    logging.TRACE: "<dim><bold><br-black>",
    logging.DEBUG: "<bold><br-black>",
    logging.INFO: "<bold><blue>",
    logging.SUCCESS: "<bold><green>",
    logging.WARNING: "<bold><yellow>",
    logging.ERROR: "<bold><br-red>",
    logging.CRITICAL: "<bold><underline><red>",
}

_default_lvlmsg_mod = {
    logging.TRACE: "<dim><br-black>",
    logging.DEBUG: "<italic><br-black>",
    logging.INFO: "<white>",
    logging.SUCCESS: "<green>",
    logging.WARNING: "<br-yellow>",
    logging.ERROR: "<br-red>",
    logging.CRITICAL: "<bold><red>",
}

# default custom tags
_default_custom_tags: Dict[str, Callable[[logging.LogRecord], str]] = {
    "level": lambda record: _default_level_mod.get(record.levelno),
    "lvlmsg": lambda record: _default_lvlmsg_mod.get(record.levelno)
}

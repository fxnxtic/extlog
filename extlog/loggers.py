import logging
from typing import Optional, Mapping

from .default import TRACE, SUCCESS


class ExtLogger(logging.Logger):
    """Logger that implements extended logging levels as 'TRACE' and 'SUCCESS'."""

    def __init__(self, name: str, level = 0):
        logging.TRACE = TRACE
        logging.SUCCESS = SUCCESS

        logging.addLevelName(logging.SUCCESS, "SUCCESS"),
        logging.addLevelName(logging.TRACE, "TRACE")

        super().__init__(name, level)
    
    def success(self, 
                msg, 
                *args, 
                exc_info = None, 
                stack_info: bool = False, 
                stacklevel: int = 1, 
                extra: Mapping[str, object] = None):
        """Log 'msg % args' with severity 'SUCCESS'.
        
        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.
        
        logger.success("Houston, we have a %s", "notable problem", exc_info=True)
        """
        if self.isEnabledFor(logging.SUCCESS):
            self._log(logging.SUCCESS, msg, args, exc_info, extra, stack_info, stacklevel)

    def trace(self, 
              msg, 
              *args,
              exc_info = None, 
              stack_info: bool = False, 
              stacklevel: int = 1, 
              extra: Mapping[str, object] = None):
        """Log 'msg % args' with severity 'TRACE'.
        
        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.
        
        logger.info("Houston, we have a %s", "notable problem", exc_info=True)
        """
        if self.isEnabledFor(logging.TRACE):
            self._log(logging.TRACE, msg, args, exc_info, extra, stack_info, stacklevel)


def getLogger(name: Optional[str] = None) -> ExtLogger:
    """
        Get a logger with the specified name (channel name), creating it
        if it doesn't yet exist. This name is a dot-separated hierarchical
        name, such as "a", "a.b", "a.b.c" or similar.

        If a PlaceHolder existed for the specified name [i.e. the logger
        didn't exist but a child of it did], replace it with the created
        logger and fix up the parent/child references which pointed to the
        placeholder to now point to the logger.
    """
    logging.setLoggerClass(ExtLogger)
    logger = logging.getLogger(name)

    return logger

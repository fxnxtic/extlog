import os
import sys
import subprocess
import logging
from typing import Optional

from extlog.utils import MultitonMeta


class ConsoleHandler(logging.StreamHandler, metaclass=MultitonMeta):
    """
    Handler for output logs to detached commandline.
    """
    def __init__(self, title: Optional[str] = 'extlog'):
        self.title = title
        self.console = subprocess.Popen(
            [sys.executable, os.path.realpath("extlog/_console.py"), self.title],
            stdin=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE,
            text=True
            )
        
        super().__init__(self.console.stdin)

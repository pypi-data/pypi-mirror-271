__all__ = [
    "CallerFrame",
    "FileMode",
    "Lock",
    "LogLevel",
    "Record",
    "Logger",
    "Manager",
    "Registry",
    "RootLogger",
    "load_config",
    "get_logger",
    "critical",
    "debug",
    "error",
    "info",
    "warning",
    "log",
    "disable",
    "shutdown",
    "formatters",
    "handlers",
    "streams",
    "__author__",
    "__description__",
    "__name__",
    "__version__"
]
__author__ = "coldsofttech"
__description__ = """
The pyloggermanager package is a vital logging framework for Python applications, providing developers with essential
tools to streamline logging operations. Its primary function is to simplify the recording and organization of log
messages, including critical information, debugging messages, errors, and warnings. By offering a centralized interface
and robust functionalities, the package facilitates efficient monitoring and troubleshooting processes.

With its intuitive interface, the pyloggermanager package enables developers to seamlessly integrate logging mechanisms
into their applications. This allows for systematic recording and categorization of log entries based on severity
levels, enhancing readability and prioritization of issues. Moreover, the package offers flexibility in customizing
logging configurations to suit specific project requirements, including formatting, output destinations, and thread
safety.

Beyond technical capabilities, the pyloggermanager package contributes to the reliability and maintainability of Python
applications. It establishes consistent logging practices, simplifying collaboration, code reviews, and issue
resolution across development teams. Overall, the pyloggermanager package is an invaluable asset for developers aiming
to implement robust logging solutions, ensuring efficient and resilient application performance.
"""
__name__ = "pyloggermanager"
__version__ = "0.1.4"

from pyloggermanager import formatters
from pyloggermanager import handlers
from pyloggermanager import streams
from pyloggermanager.__main__ import CallerFrame, FileMode, Lock, LogLevel, Record, Logger, Manager, \
    Registry, RootLogger, load_config, get_logger, critical, debug, error, info, warning, log, disable, shutdown

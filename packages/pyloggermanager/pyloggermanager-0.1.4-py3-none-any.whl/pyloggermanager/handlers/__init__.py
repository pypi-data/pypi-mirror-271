__all__ = [
    "Handler",
    "ConsoleHandler",
    "FileHandler",
    "StreamHandler",
    "StderrHandler"
]
__name__ = "pyloggermanager.handlers"
__description__ = """
The pyloggermanager.handlers package provides classes responsible for handling log records
generated within the logger manager framework. It includes various handlers for processing log
messages, directing them to different destinations, and performing actions based on logging levels.

Below listed handler classes offer flexibility and customization options for managing log records
within the logger manager framework. They enable users to define how log messages are processed,
where they are directed, and how they are formatted, catering to various logging scenarios and
deployment environments.

Overall, the pyloggermanager.handlers package enhances the functionality of the logger manager
framework by providing a robust set of handlers for managing log records effectively and efficiently.
Users can choose and configure handlers based on their specific logging needs and infrastructure requirements.
"""

from pyloggermanager.handlers.__main__ import Handler, ConsoleHandler, FileHandler, StreamHandler, StderrHandler

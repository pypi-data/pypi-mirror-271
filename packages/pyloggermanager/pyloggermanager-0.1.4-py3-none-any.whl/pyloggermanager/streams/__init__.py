__all__ = [
    "Stream",
    "StdoutStream",
    "StderrStream",
    "TerminalStream"
]
__name__ = "pyloggermanager.streams"
__description__ = """
The pyloggermanager.streams package provides classes related to handling output streams for log records
within the logger manager framework. These classes define different types of streams that log messages
can be directed to, allowing for flexible and customizable logging behaviour.

Below listed stream classes offer versatility in directing log messages to different output
channels, allowing users to customize logging behavior based on their application's requirements
and environment configuration. By supporting various stream types, the logger manager framework
enables users to control where log records are displayed or stored, facilitating effective logging
and troubleshooting processes.

Overall, the pyloggermanager.streams package enhances the functionality of the logger manager framework
by providing a range of stream classes for directing log messages to different output channels. Users can
leverage these classes to tailor their logging setup to suit their specific needs and preferences, ensuring
efficient management and processing of log records.
"""

from pyloggermanager.streams.__main__ import Stream, StdoutStream, StderrStream, TerminalStream

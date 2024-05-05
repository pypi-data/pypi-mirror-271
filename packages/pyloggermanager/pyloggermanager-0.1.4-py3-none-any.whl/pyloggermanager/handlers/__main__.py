import io
import os
import sys
from types import NoneType
from typing import Any, TextIO, Union

import pyloggermanager
from pyloggermanager.formatters import Formatter, DefaultFormatter
from pyloggermanager.streams import Stream, TerminalStream, StdoutStream

_handlersList = []


class Handler:
    """
    Base class for different log handlers used in logging systems.
    Provides methods and properties to manage handler attributes such as name,
    log level, colorization, and formatter. Also includes methods to acquire/release locks,
    close the handler, emit log records, format log records, flush buffered records,
    and retrieve a list of all handlers.
    """

    def __init__(
            self,
            name: str = None,
            level: int = 20,
            colorization=None,
            formatter: Formatter = DefaultFormatter()
    ) -> None:
        """
        Initializes the handler with optional attributes.

        :param name: Handle name.
        :type name: str
        :param level: Handler log level.
        :type level: int
        :param colorization: Colorization object for the handler.
        :type colorization: pycolorecho.ColorMapper
        :param formatter: Formatter object for formatting log records.
        :type formatter: Formatter
        """
        from pycolorecho import ColorMapper

        if not isinstance(name, Union[str, NoneType]):
            raise TypeError('name should be a string.')
        elif not isinstance(level, int):
            raise TypeError('level should be an integer.')
        elif not isinstance(colorization, Union[ColorMapper, NoneType]):
            raise TypeError('colorization should be of pycolorecho.ColorMapper type.')
        elif not issubclass(type(formatter), Formatter):
            raise TypeError('formatter should be subclass of Formatter.')

        self._name = name
        self._level = pyloggermanager.LogLevel.check_level(level)
        self._colorization = colorization
        self._formatter = formatter
        self._acquire_lock()
        try:
            _handlersList.append(self)
        finally:
            self._release_lock()

    @property
    def colorization(self):
        """
        Gets the colorization object for the handler.

        :return: Colorization object.
        """
        return self._colorization

    @colorization.setter
    def colorization(self, value) -> None:
        """
        Sets the colorization object for the handler.

        :param value: Colorization object for the handler.
        """
        from pycolorecho import ColorMapper

        if not isinstance(value, Union[ColorMapper, NoneType]):
            raise TypeError('colorization should be of pycolorecho.ColorMapper type.')

        self._colorization = value

    @property
    def formatter(self) -> Formatter:
        """
        Gets the formatter object for formatting log records.

        :return: Formatter object.
        """
        return self._formatter

    @formatter.setter
    def formatter(self, value: Formatter) -> None:
        """
        Sets the formatter object for formatting log records.

        :param value: Formatter object for the handler.
        """
        if not issubclass(type(value), Formatter):
            raise TypeError('formatter should be subclass of Formatter.')

        self._formatter = value

    @property
    def level(self) -> int:
        """
        Gets the log level for the handler.

        :return: Log level.
        """
        return self._level

    @level.setter
    def level(self, value: int) -> None:
        """
        Sets the log level for the handler.

        :param value: Log level for the handler.
        """
        if not isinstance(value, int):
            raise TypeError('level should be an integer.')

        self._level = pyloggermanager.LogLevel.check_level(value)

    @property
    def name(self) -> str:
        """
        Gets the name of the handler.

        :return: Handler name.
        """
        return self._name

    @name.setter
    def name(self, value: str | None) -> None:
        """
        Sets the name of the handler.

        :param value: Name for the handler.
        """
        if not isinstance(value, Union[str, NoneType]):
            raise TypeError('name should be a string.')

        self._name = value

    def _acquire_lock(self) -> None:
        """
        Acquires a lock for thread safety.
        """
        from pyloggermanager import Lock

        self._lock_name = Lock.generate_name()
        self._create_lock()
        Lock.acquire(self._lock_name)

    def _create_lock(self) -> None:
        """
        Creates a lock.
        """
        from pyloggermanager import Lock

        Lock.create(self._lock_name)

    def _release_lock(self) -> None:
        """
        Releases the lock acquired for thread safety.
        """
        from pyloggermanager import Lock

        Lock.release(self._lock_name)

    def close(self) -> None:
        """
        Closes the handler.
        """
        self._acquire_lock()
        try:
            if self in _handlersList:
                _handlersList.remove(self)
        finally:
            self._release_lock()

    def emit(self, record, ignore_display: bool) -> None:
        """
        Abstract method to emit a log record.

        :param ignore_display: Flag to indicate if log message should be displayed on terminal.
        :param record: Log record.
        """
        raise NotImplementedError('emit() method must be implemented in subclasses.')

    def format(self, record) -> str:
        """
        Formats a log record using the handler's formatter.

        :param record: Log record to format.
        :return: Formatted log record.
        """
        return str(self._formatter.format(record))

    def flush(self) -> None:
        """
        Flushes buffered records.
        """
        raise NotImplementedError('flush() method must be implemented in subclasses.')

    @staticmethod
    def get_handlers() -> list[Any]:
        """
        Retrieves a list of all handlers.

        :return: List of all handlers.
        """
        return _handlersList

    def handle(self, record, ignore_display: bool) -> None:
        """
        Handles a log record.

        :param ignore_display: Flag to indicate if log message should be displayed on terminal.
        :param record: Log record.
        """
        if not isinstance(record, pyloggermanager.Record):
            raise TypeError('record should be of Record type.')
        elif not isinstance(ignore_display, bool):
            raise TypeError('ignore_display should be a boolean.')

        self._acquire_lock()
        try:
            self.emit(record, ignore_display)
        finally:
            self._release_lock()


class ConsoleHandler(Handler):
    """
    Subclass of Handler representing a handler that writes log records to the console.
    Provides methods to set and retrieve the stream used for logging, close the stream,
    emit log records, and flush the stream.
    """

    def __init__(
            self,
            name: str = None,
            level: int = 20,
            colorization=None,
            formatter: Formatter = DefaultFormatter(),
            stream: Stream = TerminalStream()
    ) -> None:
        """
        Initializes a ConsoleHandler instance.

        :param name: Handle name.
        :type name: str
        :param level: Handler log level.
        :type level: int
        :param colorization: Colorization object for the handler.
        :type colorization: pycolorecho.ColorMapper
        :param formatter: Formatter object for formatting log records.
        :type formatter: Formatter
        :param stream: Stream object for the handler.
        :type stream: Stream
        """
        if not issubclass(type(stream), Stream):
            raise TypeError('stream should be subclass of Stream.')

        self._stream = stream
        super().__init__(name, level, colorization, formatter)

    @property
    def stream(self) -> Stream:
        """
        Gets the stream of the handler.

        :return: Stream of the handler.
        :rtype: Stream
        """
        return self._stream

    @stream.setter
    def stream(self, value: Stream) -> None:
        """
        Sets the stream of the handler.

        :param value: Stream for the handler.
        :type value: Stream
        """
        if not issubclass(type(value), Stream):
            raise TypeError('stream should be subclass of Stream.')

        self._stream = value

    def close(self) -> None:
        """
        Closes the stream if it has a close method.
        """
        if hasattr(self._stream, 'close'):
            self._stream.close()
        super().close()

    def emit(self, record, ignore_display: bool = True) -> None:
        """
        Emits the log record by formatting it, colorizing the message, and writing it to the stream.

        :param record: Log record to emit.
        :type record: Record
        :param ignore_display: Flag to indicate if log message should be displayed on terminal.
        :type ignore_display: bool
        """
        import pycolorecho

        formatted_record = self.format(record)
        colored_message = pycolorecho.get_colorized_message_by_mappings(
            formatted_record, mappings=self.colorization
        ) if self.colorization else formatted_record
        self._stream.write(colored_message)

    def flush(self) -> None:
        """
        Flushes the stream if it has a flush method.
        """
        if hasattr(self._stream, 'flush'):
            self._stream.flush()


class StreamHandler(Handler):
    """
    Subclass of Handler representing a handler that emits log records to a stream.
    Provides methods to set the log level, formatter, and stream, as well as to
    emit log records and flush the stream.
    """

    # Constant representing the terminator character used to terminate log records when writing
    # to the stream.
    TERMINATOR = '\n'

    def __init__(
            self,
            name: str = None,
            level: int = 20,
            colorization=None,
            formatter: Formatter = DefaultFormatter(),
            stream: Stream = StdoutStream()
    ) -> None:
        """
        Initializes a StreamHandler instance.

        :param name: Handle name.
        :type name: str
        :param level: Handler log level.
        :type level: int
        :param colorization: Colorization object for the handler.
        :type colorization: pycolorecho.ColorMapper
        :param formatter: Formatter object for formatting log records.
        :type formatter: Formatter
        :param stream: Stream object for the handler.
        :type stream: Stream
        """
        if not issubclass(type(stream), Stream):
            raise TypeError('stream should be subclass of Stream.')

        self._acquire_lock()
        try:
            self._stream = stream
        finally:
            self._release_lock()

        super().__init__(name, level, colorization, formatter)

    @property
    def stream(self) -> Stream:
        """
        Gets the stream of the handler.

        :return: Stream of the handler.
        :rtype: Stream
        """
        return self._stream

    @stream.setter
    def stream(self, value: Stream) -> None:
        """
        Sets the stream of the handler.

        :param value: Stream of the handler.
        :type value: Stream
        """
        if not issubclass(type(value), Stream):
            raise TypeError('stream should be subclass of Stream.')

        self._stream = value

    def close(self) -> None:
        """
        Closes the stream if it has a close method.
        """
        if hasattr(self._stream, 'close'):
            self._stream.close()
        super().close()

    def emit(self, record, ignore_display: bool) -> None:
        """
        Emits a log record to the stream.

        :param record: Log record to emit.
        :type record: Record
        :param ignore_display: Flag to indicate if log message should be displayed on terminal.
        :type ignore_display: bool
        """
        import pycolorecho

        formatted_record = self.format(record)
        self._stream.write(formatted_record + self.TERMINATOR)
        self.flush()

        if not ignore_display:
            colored_message = pycolorecho.get_colorized_message_by_mappings(
                formatted_record, mappings=self.colorization
            ) if self.colorization else formatted_record
            print(colored_message)

    def flush(self) -> None:
        """
        Flushes the stream if it has a flush method.
        """
        self._acquire_lock()
        try:
            if hasattr(self._stream, 'flush'):
                self._stream.flush()
        finally:
            self._release_lock()


class FileHandler(Handler):
    """
    Subclass of Handler responsible for handling log records by writing them to a file.
    Allows customization of various parameters such as file name, file mode, encoding, etc.
    """

    # Constant representing the string to terminate each log record when writing to the file.
    TERMINATOR = '\n'

    def __init__(
            self,
            name: str = None,
            level: int = 20,
            colorization=None,
            formatter: Formatter = DefaultFormatter(),
            file_name: str = 'default.log',
            file_mode: str = 'a',
            encoding: str = 'UTF-8'
    ) -> None:
        """
        Initializes a FileHandler object.

        :param name: Handle name.
        :type name: str
        :param level: Handler log level.
        :type level: int | LogLevel
        :param colorization: Colorization object for the handler.
        :type colorization: pycolorecho.ColorMapper
        :param formatter: Formatter object for formatting log records.
        :type formatter: Formatter
        :param file_name: Name of the log file. Defaults to 'default.log'.
        :type file_name: str
        :param file_mode: File mode for opening the log file. Defaults to 'a'.
        :type file_mode: int | FileMode
        :param encoding: Encoding to be used for writing to the log file. Defaults to 'UTF-8'.
        :type encoding: str
        """
        if not isinstance(file_name, str):
            raise TypeError('file_name should be a string.')
        elif not isinstance(file_mode, str):
            raise TypeError('file_mode should be a string.')
        elif not isinstance(encoding, str):
            raise TypeError('encoding should be a string.')

        self._file_name = os.fspath(file_name)
        self._file_mode = pyloggermanager.FileMode.check_mode(file_mode)
        self._encoding = encoding
        self._file_stream = None

        super().__init__(name, level, colorization, formatter)

    @property
    def encoding(self) -> str:
        """
        Gets the encoding of the handler.

        :return: Encoding of the handler.
        :rtype: str
        """
        return self._encoding

    @encoding.setter
    def encoding(self, value: str) -> None:
        """
        Sets the encoding of the handler.

        :param value: Encoding of the handler.
        :type value: str
        """
        if not isinstance(value, str):
            raise TypeError('encoding should be a string.')

        self._encoding = value

    @property
    def filemode(self) -> str:
        """
        Gets the file mode for opening the file handler.

        :return: File mode.
        :rtype: str
        """
        return self._file_mode

    @filemode.setter
    def filemode(self, value: str) -> None:
        """
        Sets the file mode for opening the file handler.

        :param value: File mode.
        :type value: str
        """
        if not isinstance(value, str):
            raise TypeError('file_mode should be a string.')

        self._file_mode = pyloggermanager.FileMode.check_mode(value)

    @property
    def filename(self) -> str:
        """
        Gets the file name of the handler.

        :return: File name of the handler.
        :rtype: str
        """
        return self._file_name

    @filename.setter
    def filename(self, value: str) -> None:
        """
        Sets the file name of the handler.

        :param value: File name of the handler.
        :type value: str
        """
        if not isinstance(value, str):
            raise TypeError('file_name should be a string.')

        self._file_name = os.fspath(value)

    def _close_file_stream(self) -> None:
        """
        Closes the file stream used for writing log records.
        """
        self._acquire_lock()
        try:
            if self._file_stream is not None:
                self._file_stream.close()
        finally:
            self._release_lock()

    def _open_file_stream(self) -> None:
        """
        Opens the file stream for writing log records.
        """
        self._acquire_lock()
        try:
            self._file_stream = io.open(self._file_name, self._file_mode, encoding=self._encoding)
        finally:
            self._release_lock()

    def close(self) -> None:
        """
        Closes the file stream used for writing log records.
        """
        self._close_file_stream()
        super().close()

    def emit(self, record, ignore_display: bool) -> None:
        """
        Emits a log record by writing it to the log file.

        :param record: Log record to emit.
        :type record: Record
        :param ignore_display: Flag to indicate if log message should be displayed on terminal.
        :type ignore_display: bool
        """
        import pycolorecho

        formatted_record = self.format(record)
        self._open_file_stream()
        self._acquire_lock()
        try:
            self._file_stream.write(formatted_record + self.TERMINATOR)
            self._file_stream.flush()
        finally:
            self._release_lock()
            self._close_file_stream()

        if not ignore_display:
            colored_message = pycolorecho.get_colorized_message_by_mappings(
                formatted_record, mappings=self.colorization
            ) if self.colorization else formatted_record
            print(colored_message)

    def flush(self) -> None:
        """
        Flushes the file stream used for writing log records.
        """
        self._acquire_lock()
        try:
            if self._file_stream is not None:
                self._file_stream.flush()
        finally:
            self._release_lock()


class StderrHandler(Handler):
    """
    Subclass of Handler responsible for handling log records by writing them to the standard error stream (stderr).
    """

    def __init__(self, level: int = 30) -> None:
        """
        Initializes a StderrHandler object.

        :param level: Handler log level. Defaults to WARNING level (30).
        :type level: int
        """
        super().__init__(level=level)

    @property
    def stream(self) -> TextIO:
        """
        Gets the standard error stream (stderr).

        :return: Standard error stream (stderr).
        :rtype: TextIO
        """
        return sys.stderr

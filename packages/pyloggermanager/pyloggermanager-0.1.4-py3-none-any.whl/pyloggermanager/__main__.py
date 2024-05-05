import inspect
import io
import json
import os
import random
import string
import sys
import threading
import traceback
from datetime import datetime
from types import FrameType, TracebackType, NoneType
from typing import Any, Optional, Tuple, Type, Union

from pyloggermanager.formatters import Formatter, DefaultFormatter, DEFAULT_FORMAT, DATE_FORMAT
from pyloggermanager.handlers import Handler, StderrHandler, FileHandler, StreamHandler
from pyloggermanager.streams import Stream


class CallerFrame:
    """
    This class represents caller details such as class name, file name, function name,
    module name, and path name based on the caller's frame information. It provides a
    method to retrieve caller details from a given frame.
    """

    def __init__(self):
        """Initializes the 'CallerFrame' object with default attribute values."""
        self.class_name = 'Unknown Class'
        self.file_name = 'Unknown File'
        self.function_name = 'Unknown Function'
        self.module_name = 'Unknown Module'
        self.path_name = 'Unknown Path'

    @classmethod
    def get_caller_details(cls, frame: FrameType) -> 'CallerFrame':
        """
        Retrieves caller details from the given frame.

        :param frame: Frame object containing caller information.
        :type frame: FrameType
        :return: Caller details
        :rtype: CallerFrame
        """
        if not isinstance(frame, FrameType):
            raise TypeError('frame should be of FrameType type.')

        caller_frame = cls()

        while frame:
            # Extract file name without extension
            caller_frame.file_name = os.path.splitext(os.path.basename(frame.f_globals.get('__file__', '')))[0]
            caller_frame.module_name = os.path.splitext(caller_frame.file_name)[0]
            caller_frame.path_name = frame.f_globals.get('__file__', '')

            # Check if the frame contains 'self' in locals (indicating a method call)
            if 'self' in frame.f_locals:
                caller_frame.class_name = frame.f_locals['self'].__class__.__name__
                caller_frame.function_name = frame.f_code.co_name
                break

            frame = frame.f_back

        return caller_frame


class FileMode:
    """
    This class represents file modes supported by the Python open() function
    for reading, writing, and appending to the files. It provides methods to retrieve
    default file mode, get the file mode mappings, check if a mode is valid, set
    default file mode, and get readable and writable modes.
    """
    # Refer to https://docs.python.org/3/library/functions.html#open for supported file modes
    READ: str = 'r'  # Constant representing the read file mode
    READ_PLUS: str = 'r+'  # Constant representing the read/write file mode
    WRITE: str = 'w'  # Constant representing the write file mode
    WRITE_PLUS: str = 'w+'  # Constant representing the read/write file mode
    EXCLUSIVE_CREATE: str = 'x'  # Constant representing the exclusive creation file mode
    APPEND: str = 'a'  # Constant representing the append file mode
    APPEND_PLUS: str = 'a+'  # Constant representing the read/append file mode
    BINARY: str = 'b'  # Constant representing the binary file mode
    READ_BINARY: str = 'rb'  # Constant representing the read binary file mode
    READ_WRITE_BINARY: str = 'r+b'  # Constant represent the read/write binary file mode
    TEXT: str = 't'  # Constant representing the text file mode
    UPDATE: str = '+'  # Constant representing the update file mode

    _default_mode: str = APPEND  # Default file mode set to append 'a'

    # Dictionary mapping file mode strings to their corresponding names
    _mode_to_name = {
        READ: 'READ',
        READ_PLUS: 'READ_PLUS',
        WRITE: 'WRITE',
        WRITE_PLUS: 'WRITE_PLUS',
        EXCLUSIVE_CREATE: 'EXCLUSIVE_CREATE',
        APPEND: 'APPEND',
        APPEND_PLUS: 'APPEND_PLUS',
        BINARY: 'BINARY',
        READ_BINARY: 'READ_BINARY',
        READ_WRITE_BINARY: 'READ_WRITE_BINARY',
        TEXT: 'TEXT',
        UPDATE: 'UPDATE'
    }

    # Dictionary mapping file mode names to their corresponding strings
    _name_to_mode = {v: k for k, v in _mode_to_name.items()}

    @classmethod
    def check_mode(cls, mode: str) -> str:
        """
        Checks if the provided mode exists and returns the same value if exists, else raise ValueError.

        :param mode: The file mode to check
        :type mode: str
        :return: Provided file mode if it exists
        :rtype: str
        :raises ValueError: If the provided mode does not exist
        """
        if not isinstance(mode, str):
            raise TypeError('mode should be a string.')

        if cls.is_valid_mode(mode):
            return mode
        else:
            raise ValueError(f'Invalid file mode: {mode}')

    @classmethod
    def get_default_mode(cls) -> str:
        """
        Returns the default file mode

        :return: Default file mode
        :rtype: str
        """
        return cls._default_mode

    @classmethod
    def get_file_mode(cls, mode_str: str) -> str:
        """
        Returns the file mode string corresponding to the provided mode name

        :param mode_str: File mode name
        :type mode_str: str
        :return: File mode string
        :rtype: str
        """
        if not isinstance(mode_str, str):
            raise TypeError('mode_str should be a string.')

        combined_modes = {**cls._mode_to_name, **cls._name_to_mode}
        result = combined_modes.get(mode_str)
        if result is None:
            raise ValueError(f'Mode "{mode_str}" is not a valid value.')
        return result

    @classmethod
    def get_file_modes(cls) -> dict:
        """
        Returns a dictionary mapping file mode names to their corresponding strings

        :return: File mode mappings
        :rtype: dict
        """
        return cls._name_to_mode.copy()

    @classmethod
    def get_readable_modes(cls) -> dict:
        """
        Returns a dictionary of reading file modes and their corresponding strings

        :return: Readable file modes
        :rtype: dict
        """
        return {
            'READ': cls.READ,
            'READ_PLUS': cls.READ_PLUS,
            'WRITE_PLUS': cls.WRITE_PLUS,
            'APPEND_PLUS': cls.APPEND_PLUS,
            'READ_BINARY': cls.READ_BINARY,
            'READ_WRITE_BINARY': cls.READ_WRITE_BINARY
        }

    @classmethod
    def get_writable_modes(cls) -> dict:
        """
        Returns a dictionary of writable file modes and their corresponding strings

        :return: Writable file modes
        :rtype: dict
        """
        return {
            'WRITE': cls.WRITE,
            'WRITE_PLUS': cls.WRITE_PLUS,
            'APPEND': cls.APPEND,
            'APPEND_PLUS': cls.APPEND_PLUS
        }

    @classmethod
    def is_valid_mode(cls, mode: str) -> bool:
        """
        Checks if the provided mode string is a valid file mode

        :param mode: File mode string
        :type mode: str
        :return: True if valid, False otherwise
        :rtype: bool
        """
        if not isinstance(mode, str):
            raise TypeError('mode should be a string.')

        try:
            return cls.get_file_mode(mode) is not None
        except ValueError:
            return False

    @classmethod
    def set_default_mode(cls, mode: str) -> None:
        """
        Sets the default file mode

        :param mode: Default file mode
        :type mode: str
        :return: None
        """
        if not isinstance(mode, str):
            raise TypeError('mode should be a string.')

        if mode not in cls._mode_to_name:
            raise ValueError(f'Mode "{mode}" is not a valid value.')
        cls._default_mode = mode


class Lock:
    """
    This class provides a simple interface to manage locks using the Python threading module.
    It allows acquiring, creating, checking if a lock is locked, and releasing locks.
    """

    _locks = {}  # Dictionary to store locks created by their names

    @classmethod
    def _get_lock(cls, name: str) -> threading.RLock:
        """
        Retrieves the lock object with the given name.

        :param name: Name of the lock to retrieve.
        :type name: str
        :return: The lock object.
        :rtype: threading.RLock
        """
        if name.upper() in cls._locks:
            return cls._locks[name.upper()]
        else:
            raise ValueError(f'Lock with name "{name}" not found.')

    @classmethod
    def acquire(cls, name: str, blocking: bool = True, timeout: float = -1) -> bool:
        """
        Acquires the lock with the given name.

        :param name: Name of the lock.
        :type name: str
        :param blocking: Whether to block while waiting for the lock. Defaults to 'True'.
        :type blocking: bool
        :param timeout: Timeout for acquiring the lock. Defaults to '-1'.
        :type timeout: float
        :return: True if the lock was acquired successfully, False otherwise.
        :rtype: bool
        """
        lock = cls._get_lock(name)
        with lock:
            return lock.acquire(blocking, timeout)

    @classmethod
    def create(cls, name: str) -> None:
        """
        Creates a new lock with the given name.

        :param name: Name of the lock to create.
        :type name: str
        :return: None
        """
        cls._locks[name.upper()] = threading.RLock()

    @staticmethod
    def generate_name(length: int = 10) -> str:
        """
        Generate a random name for a lock of specified length.

        :param length: Length of the lock name. Defaults to 10.
        :type length: int
        :return: Random generated lock name.
        :rtype: str
        """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    @classmethod
    def locked(cls, name: str) -> bool:
        """
        Checks if the lock with the given name is currently locked.

        :param name: Name of the lock to check.
        :type name: str
        :return: True if the lock is currently locked, False otherwise.
        :rtype: bool
        """
        lock = cls._get_lock(name)
        if str(lock).startswith('<unlocked'):
            return False
        elif str(lock).startswith('<locked'):
            return True

    @classmethod
    def release(cls, name: str) -> None:
        """
        Releases the lock with the given name.

        :param name: Name of the lock to release.
        :type name: str
        :return: None
        """
        try:
            cls._get_lock(name).release()
        except RuntimeError:
            pass


class LogLevel:
    """
    This class represents different log levels used in logging systems.
    It provides methods to check if a log level is valid, get default log level,
    get log level mappings, remove log levels, set default log level, and set custom log levels.
    """

    # Constants representing log levels
    DEBUG: int = 10
    INFO: int = 20
    WARNING: int = 30
    ERROR: int = 40
    CRITICAL: int = 50

    # Default log level
    _default_level: int = INFO

    # Dictionary mapping log level integers to their corresponding names
    _level_to_name = {
        DEBUG: 'DEBUG',
        INFO: 'INFO',
        WARNING: 'WARNING',
        ERROR: 'ERROR',
        CRITICAL: 'CRITICAL'
    }

    # Dictionary mapping log level names to their corresponding integers
    _name_to_level = {v: k for k, v in _level_to_name.items()}

    @classmethod
    def check_level(cls, level: int) -> int:
        """
        Checks if the provided level exists and returns the same value if exists, else raise ValueError.

        :param level: The log level to check
        :type level: int
        :return: Provided level if it exists
        :rtype: int
        :raises ValueError: If the provided level does not exist
        """
        if not isinstance(level, int):
            raise TypeError('level should be an integer.')

        if cls.is_valid_level(level):
            return level
        else:
            raise ValueError(f'Invalid level: {level}')

    @classmethod
    def get_default_level(cls) -> str:
        """
        Returns the default log level as a string.

        :return: Default log level
        :rtype: str
        """
        return cls._level_to_name[cls._default_level]

    @classmethod
    def get_level(cls, level: int | str) -> str | int:
        """
        Returns the log level name if an integer level is provided,
        or returns the log level integer if a string level is provided.

        :param level: Log level (integer or string)
        :type level: int | str
        :return: Log level name if level is integer, otherwise log level integer
        :rtype: str | int
        :raises TypeError: If the provided level is not an integer or a string
        """
        if isinstance(level, int):
            return cls._level_to_name.get(level, f'Level {level}')
        elif isinstance(level, str):
            return cls._name_to_level.get(level, '')
        else:
            raise TypeError(f'Level should be either integer or string: {level}')

    @classmethod
    def get_levels(cls) -> dict:
        """
        Returns a dictionary mapping log level integers to their corresponding names, sorted by level.

        :return: Log level mappings
        :rtype: dict
        """
        return {key: cls._level_to_name[key] for key in sorted(cls._level_to_name.keys())}

    @classmethod
    def get_next_level(cls, current_level: int) -> int | None:
        """
        Returns the next log level integer after the provided current level,
        or None if it is the highest level.

        :param current_level: Current log level integer
        :type current_level: int
        :return: Next log level integer
        :rtype: int
        """
        if not isinstance(current_level, int):
            raise TypeError('current_level should be an integer.')

        sorted_levels = sorted(cls._level_to_name)
        try:
            index = sorted_levels.index(current_level)
            return sorted_levels[index + 1]
        except (IndexError, ValueError):
            return None

    @classmethod
    def get_previous_level(cls, current_level: int) -> int | None:
        """
        Returns the previous log level integer before the provided current level,
        or None if it is the lowest level.

        :param current_level: Current log level integer
        :type current_level: int
        :return: Previous log level integer
        :rtype: int
        """
        if not isinstance(current_level, int):
            raise TypeError('current_level should be an integer.')

        sorted_levels = sorted(cls._level_to_name)
        try:
            index = sorted_levels.index(current_level)
            return sorted_levels[index - 1] if index > 0 else None
        except (IndexError, ValueError):
            return None

    @classmethod
    def is_valid_level(cls, level: int | str) -> bool:
        """
        Checks if the provided log level (integer or string) is a valid log level.

        :param level: Log level (integer or string)
        :return: True if valid, False otherwise
        :rtype: bool
        """
        if isinstance(level, int):
            return level in cls._level_to_name
        elif isinstance(level, str):
            return level in cls._name_to_level
        else:
            raise TypeError(f'Level should be either integer or a valid string: {level}')

    @classmethod
    def remove_level(cls, level: int | str) -> None:
        """
        Removes the log level mapping for the specified level.

        :param level: The level value or name of the log level to remove
        :type level: int | str
        :return: None
        :raises ValueError: If the log level to remove does not exist
        """
        if not isinstance(level, Union[int, str]):
            raise TypeError('level should either be an integer or a string.')

        level_number = level if isinstance(level, int) else cls.get_level(level)
        level_name = level if isinstance(level, str) else cls.get_level(level)
        if level_number is not None and level_name is not None:
            try:
                del cls._name_to_level[level_name]
                del cls._level_to_name[level_number]
            except KeyError:
                raise ValueError(f'No mapping found for log level "{level}".')
        else:
            raise ValueError(f'No mapping found for log level "{level}".')

    @classmethod
    def set_default_level(cls, level: int | str) -> None:
        """
        Sets the default log level based on the provided integer or string level.

        :param level: Default log level (integer or string)
        :type level: int | str
        :return: None
        :raises ValueError: If the provided level is invalid
        """
        if not isinstance(level, Union[int, str]):
            raise TypeError('level should be either an integer or a string.')

        if cls.is_valid_level(level):
            cls._default_level = cls._name_to_level.get(level) if isinstance(level, str) else level
        else:
            raise ValueError(f'Invalid level: {level}')

    @classmethod
    def set_level(cls, level: int, level_name: str) -> None:
        """
        Sets a custom log level with the provided level integer and name.

        :param level: Log level integer
        :type level: int
        :param level_name: Log level name
        :type level_name: str
        :return: None
        """
        if not isinstance(level, int):
            raise TypeError('level should be an integer.')
        elif not isinstance(level_name, str):
            raise TypeError('level_name should be a string.')

        cls._level_to_name[level] = level_name
        cls._name_to_level[level_name] = level


class Record:
    """
    Represents a log record with various attributes such as message, logger name,
    level name, caller frame information, execution information, stack information, and
    thread/process details. Provides methods to serialize the record to a dictionary and JSON format.
    """

    def __init__(
            self,
            message: str,
            logger_name: str,
            level_number: int,
            caller_frame: "CallerFrame",
            exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]] = None,
            stack_info: Optional[str] = None
    ) -> None:
        """
        Constructs a new 'Record' object with the provided parameters.

        :param message: Log message
        :type message: str
        :param logger_name: Name of the Logger
        :type logger_name: str
        :param level_number: Numeric value of the log level
        :type level_number: int
        :param caller_frame: Caller frame details
        :type caller_frame: CallerFrame
        :param exec_info: Execution information, defaults to None
        :type exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]], optional
        :param stack_info: Stack information, defaults to None
        :type stack_info: Optional[str], optional
        """
        if not isinstance(message, str):
            raise TypeError('message should be a string.')
        elif not isinstance(logger_name, str):
            raise TypeError('logger_name should be a string.')
        elif not isinstance(level_number, int):
            raise TypeError('level_number should be an integer.')
        elif not isinstance(caller_frame, CallerFrame):
            raise TypeError('caller_frame should be of CallerFrame type.')
        elif not isinstance(stack_info, Union[str, NoneType]):
            raise TypeError('stack_info should be a string.')
        elif not isinstance(exec_info, Union[Tuple, NoneType]):
            if exec_info:
                if not len(exec_info) == 3 or isinstance(exec_info[0], type) or \
                        isinstance(exec_info[0], BaseException) or \
                        isinstance(exec_info[1], BaseException) or \
                        isinstance(exec_info[2], Union[TracebackType, None]):
                    raise TypeError(
                        'exec_info should be of Tuple[Type[BaseException], BaseException, Optional[TracebackType]]'
                    )

        self._time = datetime.utcnow()
        self._message = message
        self._logger_name = logger_name
        self._level_number = LogLevel.check_level(level_number)
        self._level_name = LogLevel.get_level(self._level_number)
        self._file_name = caller_frame.file_name
        self._class_name = caller_frame.class_name
        self._function_name = caller_frame.function_name
        self._module_name = caller_frame.module_name
        self._path_name = caller_frame.path_name
        self._exec_info = exec_info
        self._stack_info = stack_info
        self._thread = threading.get_ident() if threading else None
        self._thread_name = threading.current_thread().name if threading else None
        self._process_id = os.getpid() if hasattr(os, 'getpid') else None

    @property
    def time(self) -> datetime:
        """
        Property representing the timestamp of the log record.
        """
        return self._time

    @property
    def message(self) -> str:
        """
        Property representing the log message.
        """
        return self._message

    @message.setter
    def message(self, value: str) -> None:
        """
        Setter for the log message.

        :param value: New log message
        :type value: str
        """
        if not isinstance(value, str):
            raise TypeError('message should be a string.')

        self._message = value

    @property
    def logger_name(self) -> str:
        """
        Property representing the name of the logger.
        """
        return self._logger_name

    @logger_name.setter
    def logger_name(self, value: str) -> None:
        """
        Setter for the name of the logger.

        :param value: New logger name
        :type value: str
        """
        if not isinstance(value, str):
            raise TypeError('logger_name should be a string.')

        self._logger_name = value

    @property
    def level_number(self) -> int:
        """
        Property representing the numeric value of the log level.
        """
        return self._level_number

    @level_number.setter
    def level_number(self, value: int) -> None:
        """
        Setter for the numeric value of the log level.

        :param value: New numeric log level value
        :type value: int
        """
        if not isinstance(value, int):
            raise TypeError('level_number should be an integer.')

        self._level_number = LogLevel.check_level(value)
        self._level_name = LogLevel.get_level(value)

    @property
    def level_name(self) -> str:
        """
        Property representing the name of the log level.
        """
        return self._level_name

    @property
    def file_name(self) -> str:
        """
        Property representing the name of the file where the log occurred.
        """
        return self._file_name

    @file_name.setter
    def file_name(self, value: str) -> None:
        """
        Setter for the name of the file where the log occurred.

        :param value: New file name
        :type value: str
        """
        if not isinstance(value, str):
            raise TypeError('file_name should be a string.')

        self._file_name = value

    @property
    def class_name(self) -> str:
        """
        Property representing the name of the class where the log occurred.
        """
        return self._class_name

    @class_name.setter
    def class_name(self, value: str) -> None:
        """
        Setter for the name of the class where the log occurred.

        :param value: New class name
        :type value: str
        """
        if not isinstance(value, str):
            raise TypeError('class_name should be a string.')

        self._class_name = value

    @property
    def function_name(self) -> str:
        """
        Property representing the name of the function/method where the log occurred.
        """
        return self._function_name

    @function_name.setter
    def function_name(self, value: str) -> None:
        """
        Setter for the name of the function/method where the log occurred.

        :param value: New function/method name
        :type value: str
        """
        if not isinstance(value, str):
            raise TypeError('function_name should be a string.')

        self._function_name = value

    @property
    def module_name(self) -> str:
        """
        Property representing the name of the module where the log occurred.
        """
        return self._module_name

    @module_name.setter
    def module_name(self, value: str) -> None:
        """
        Setter for the name of the module where the log occurred.

        :param value: New module name
        :type value: str
        """
        if not isinstance(value, str):
            raise TypeError('module_name should be a string.')

        self._module_name = value

    @property
    def path_name(self) -> str:
        """
        Property representing the path of the file where the log occurred.
        """
        return self._path_name

    @path_name.setter
    def path_name(self, value: str) -> None:
        """
        Setter for the path of the file where the log occurred.

        :param value: New path name
        :type value: str
        """
        if not isinstance(value, str):
            raise TypeError('path_name should be a string.')

        self._path_name = value

    @property
    def exec_info(self) -> Tuple[Type[BaseException], BaseException, Optional[TracebackType]] | None:
        """
        Property representing the execution information associated with the log record.
        """
        return self._exec_info

    @exec_info.setter
    def exec_info(self, value: Tuple[Type, BaseException, Optional[TracebackType]]) -> None:
        """
        Setter for the execution information associated with the log record.

        :param value: New execution information
        :type value: Tuple[Type, BaseException, Optional[TracebackType]]
        """
        if not isinstance(value, Union[Tuple, NoneType]):
            if value:
                if not len(value) == 3 or isinstance(value[0], type) or \
                        isinstance(value[0], BaseException) or \
                        isinstance(value[1], BaseException) or \
                        isinstance(value[2], Union[TracebackType, NoneType]):
                    raise TypeError(
                        'exec_info should be of Tuple[Type[BaseException], BaseException, Optional[TracebackType]]'
                    )

        self._exec_info = value

    @property
    def stack_info(self) -> str:
        """
        Property representing the stack information associated with the log record.
        """
        return self._stack_info

    @stack_info.setter
    def stack_info(self, value: str) -> None:
        """
        Setter for the stack information associated with the log record.

        :param value: New stack information
        :type value: str
        """
        if not isinstance(value, str):
            raise TypeError('stack_info should be a string.')

        self._stack_info = value

    @property
    def thread(self) -> int | None:
        """
        Property representing the thread ID associated with the log record.
        """
        return self._thread

    @property
    def thread_name(self) -> str | None:
        """
        Property representing the name of the thread associated with the log record.
        """
        return self._thread_name

    @property
    def process_id(self) -> int | None:
        """
        Property representing the process ID associated with the log record.
        """
        return self._process_id

    @staticmethod
    def json_serializer(obj: Any) -> Union[str, None]:
        """
        Static method to serialize objects to JSON format.
        :param obj: Object to be serialized
        :type obj: Any
        :return: Serialized object in JSON format
        :rtype: Union[str, None]
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        # raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    def to_dict(self) -> dict:
        """
        Converts the 'Record' object to a dictionary.
        :return: Dictionary representation of the 'Record' object
        :rtype: dict
        """
        return {
            'time': self.time,
            'message': self.message,
            'logger_name': self.logger_name,
            'level_name': self.level_name,
            'level_number': self.level_number,
            'file_name': self.file_name,
            'class_name': self.class_name,
            'function_name': self.function_name,
            'module_name': self.module_name,
            'path_name': self.path_name,
            'exec_info': self.exec_info,
            'stack_info': self.stack_info,
            'thread': self.thread,
            'thread_name': self.thread_name,
            'process_id': self.process_id
        }

    def to_json(self) -> str:
        """
        Converts the 'Record' object to JSON string.
        :return: JSON string representation of the 'Record' object
        :rtype: str
        """
        return json.dumps(self.to_dict(), indent=4, default=Record.json_serializer)


class Logger:
    """
    Represents a logger object with various attributes and methods for logging message.
    """

    def __init__(self, name: str, level: int = LogLevel.INFO) -> None:
        """
        Initializes a new Logger object.

        :param name: The name of the logger.
        :type name: str
        :param level: The logging level, defaults to LogLevel.INFO.
        :type level: int, optional
        """
        if not isinstance(name, str):
            raise TypeError('name should be a string.')
        elif not isinstance(level, int):
            raise TypeError('level should be an integer.')

        self._name = name
        self._level = LogLevel.check_level(level)
        self._root = None
        self._parent = None
        self._propagate = True
        self._handlers = []
        self._cache = {}
        self._disabled = False
        self._lock_name = None
        self._manager = Manager(self)

    @property
    def cache(self) -> dict:
        """
        Gets the cache dictionary.

        :return: The cache dictionary.
        :rtype: dict
        """
        return self._cache

    @cache.setter
    def cache(self, value: dict) -> None:
        """
        Sets the cache dictionary.

        :param value: The new cache dictionary.
        :type value: dict
        """
        if not isinstance(value, dict):
            raise TypeError('cache should be a dict.')

        self._cache = value

    @property
    def disabled(self) -> bool:
        """
        Indicates whether the logger is disabled or not.
        """
        return self._disabled

    @disabled.setter
    def disabled(self, value: bool) -> None:
        """
        Sets the disabled status of the logger.

        :param value: The new disabled status for the logger.
        :type value: bool
        """
        if not isinstance(value, bool):
            raise TypeError('disabled should be a boolean.')

        self._disabled = value

    @property
    def handlers(self) -> list:
        """
        The list of handlers associated with the logger.
        """
        return self._handlers

    @handlers.setter
    def handlers(self, value: list) -> None:
        """
        Sets the list of handlers associated with the logger.

        :param value: The new list of handlers for the logger.
        :type value: list
        """
        if not isinstance(value, list):
            raise TypeError('handlers should be a list.')

        self._handlers = value

    @property
    def level(self) -> int:
        """
        The logging level of the logger.
        """
        return self._level

    @level.setter
    def level(self, value: int) -> None:
        """
        Sets the logging level of the logger.

        :param value: The new logging level for the logger.
        :type value: int
        """
        if not isinstance(value, int):
            raise TypeError('level should be an integer.')

        self._level = LogLevel.check_level(value)
        self.manager.clear_cache()

    @property
    def lock_name(self) -> str:
        """
        Gets the name of the lock used for thread safety.

        :return: The name of the lock.
        :rtype: str
        """
        return self._lock_name

    @lock_name.setter
    def lock_name(self, value: str) -> None:
        """
        Sets the name of the lock used for thread safety.

        :param value: The new name for the lock.
        :type value: str
        """
        if not isinstance(value, str):
            raise TypeError('lock_name should be a string.')

        self._lock_name = value

    @property
    def manager(self) -> 'Manager':
        """
        The manager associated with the logger.
        """
        return self._manager

    @manager.setter
    def manager(self, value: 'Manager') -> None:
        """
        Sets the manager associated with the logger.

        :param value: The new manager for the logger.
        :type value: 'Manager'
        """
        if not isinstance(value, Manager):
            raise TypeError('manager should be of Manager type.')

        self._manager = value

    @property
    def name(self) -> str:
        """
        The name of the logger.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Sets the name of the logger.

        :param value: The new name for the logger.
        :type value: str
        """
        if not isinstance(value, str):
            raise TypeError('name should be a string.')

        self._name = value

    @property
    def parent(self) -> 'Logger':
        """
        The parent logger in the logger hierarchy.
        """
        return self._parent

    @parent.setter
    def parent(self, value: 'Logger') -> None:
        """
        Sets the parent logger in the logger hierarchy.

        :param value: The new parent logger for the logger.
        :type value: 'Logger'
        """
        if not isinstance(value, Logger):
            raise TypeError('logger should be of Logger type.')

        self._parent = value

    @property
    def root(self) -> 'Logger':
        """
        The root logger associated with the logger hierarchy.
        """
        return self._root

    @root.setter
    def root(self, value: 'Logger') -> None:
        """
        Sets the root logger associated with the logger hierarchy.

        :param value: The new root logger for the logger hierarchy.
        :type value: 'Logger'
        """
        if not issubclass(type(value), Logger):
            raise TypeError('root should be a subclass of Logger.')

        self._root = value

    def _acquire_lock(self) -> None:
        """
        Acquires a lock for thread safety.

        :return: None
        """
        self.lock_name = Lock.generate_name()
        self._create_lock()
        Lock.acquire(self.lock_name)

    def _create_lock(self) -> None:
        """
        Creates a lock.

        :return: None
        """
        Lock.create(self.lock_name)

    @staticmethod
    def _is_internal_frame(frame: FrameType) -> bool:
        """
        Checks if the given frame is internal to the logger or part of the Python import system.

        :param frame: The frame to check.
        :type frame: FrameType
        :return: True if the frame is internal to the logger or part of the Python import system, False otherwise.
        :rtype: bool
        """
        if not isinstance(frame, FrameType):
            raise TypeError('frame should be of FrameType type.')

        file_name = os.path.normcase(frame.f_code.co_filename)
        return file_name == os.path.normcase(inspect.getfile(Logger)) or (
                'importlib' in file_name and '_bootstrap' in file_name
        )

    def _log(
            self,
            level: int,
            message: str,
            ignore_display: bool = False,
            exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]] = None,
            stack_info: bool = False,
            stack_level: int = 1
    ) -> None:
        """
        Logs a message at the specified level with additional information.

        :param level: The log level.
        :type level: int
        :param message: The log message.
        :type message: str
        :param ignore_display: Whether to ignore display settings.
        :type ignore_display: bool, optional
        :param exec_info: Information about the exception, if any.
        :type exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]], optional
        :param stack_info: Whether to include stack information.
        :type stack_info: bool, optional
        :param stack_level: The level of stack information to include.
        :type stack_level: int, optional
        :return: None
        """
        if not isinstance(message, str):
            raise TypeError('message should be a string.')
        elif not isinstance(level, int):
            raise TypeError('level should be an integer.')
        elif not isinstance(ignore_display, bool):
            raise TypeError('ignore_display should be a boolean.')
        elif not isinstance(stack_info, bool):
            raise TypeError('stack_info should be a boolean.')
        elif not isinstance(stack_level, int):
            raise TypeError('stack_level should be an integer.')
        elif not isinstance(exec_info, Union[Tuple, NoneType]):
            if exec_info:
                if not len(exec_info) == 3 or isinstance(exec_info[0], type) or \
                        isinstance(exec_info[0], BaseException) or \
                        isinstance(exec_info[1], BaseException) or \
                        isinstance(exec_info[2], Union[TracebackType, NoneType]):
                    raise TypeError(
                        'exec_info should be of Tuple[Type[BaseException], BaseException, Optional[TracebackType]]'
                    )

        s_info = None
        if os.path.normcase(inspect.getfile(Logger)):
            caller_frame, s_info = self.find_caller(stack_info, stack_level)
        else:
            caller_frame = CallerFrame()

        if exec_info:
            if isinstance(exec_info, BaseException):
                exec_info = (type(exec_info), exec_info, exec_info.__traceback__)
            elif not isinstance(exec_info, tuple):
                exec_info = sys.exc_info()

        record = self.make_record(self.name, level, message, caller_frame, exec_info, s_info)
        self.handle(record, ignore_display)

    def _release_lock(self) -> None:
        """
        Releases the lock acquired for thread safety.

        :return: None
        """
        Lock.release(self.lock_name)

    def add_handler(self, handler: Handler) -> None:
        """
        Adds a handler to the logger's list of handlers after acquiring the lock.

        :param handler: Handler object to add.
        :return: None
        """
        if not issubclass(type(handler), Handler):
            raise TypeError('handler should be a subclass of Handler.')

        self._acquire_lock()
        try:
            if handler not in self._handlers:
                self._handlers.append(handler)
        finally:
            self._release_lock()

    def call_handlers(self, record: Record, ignore_display: bool) -> None:
        """
        Calls the handlers associated with the logger.

        :param record: The log record to be handled.
        :type record: Record
        :param ignore_display: Flag indicating whether to ignore display settings.
        :type ignore_display: bool
        :return: None
        """
        if not isinstance(record, Record):
            raise TypeError('record should be of Record type.')
        elif not isinstance(ignore_display, bool):
            raise TypeError('ignore_display should be a boolean.')

        # Initialize callers_found to track the number of callers
        callers_found = 0

        # Traverse through the logger and its ancestors
        caller = self
        while caller:
            # Iterate through handlers associated with the current logger
            for handler in caller._handlers:
                # Increment callers_found for each handler found
                callers_found += 1
                # Check if the log record level is equal to or higher than the handler level
                if record.level_number >= handler.level:
                    # Call the handler's handle method with the log record
                    handler.handle(record, ignore_display)

            # Check if propagation should stop
            if not caller._propagate:
                caller = None
            else:
                # Move to the parent logger
                caller = caller.parent

        # If no handlers were found in the traversal
        if callers_found == 0:
            # Create a default stderr handler
            stderr_handler = StderrHandler(LogLevel.WARNING)
            # Check if the log record level is equal to or higher than the stderr handler level
            if stderr_handler and record.level_number >= stderr_handler.level:
                # Call the stderr handler's handle method with the log record
                stderr_handler.handle(record, ignore_display)

    def critical(
            self,
            message: str,
            ignore_display: bool = False,
            exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]] = None,
            stack_info: bool = False,
            stack_level: int = 1
    ) -> None:
        """
        Logs a message with CRITICAL level.

        :param message: The log message.
        :type message: str
        :param ignore_display: Whether to ignore display settings.
        :type ignore_display: bool, optional
        :param exec_info: Information about the exception, if any.
        :type exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]], optional
        :param stack_info: Whether to include stack information.
        :type stack_info: bool, optional
        :param stack_level: The level of stack information to include.
        :type stack_level: int, optional
        :return: None
        """
        if self.is_enabled_for(LogLevel.CRITICAL):
            self._log(LogLevel.CRITICAL, message, ignore_display, exec_info, stack_info, stack_level)

    def debug(
            self,
            message: str,
            ignore_display: bool = True,
            exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]] = None,
            stack_info: bool = False,
            stack_level: int = 1
    ) -> None:
        """
        Logs a message with DEBUG level.

        :param message: The log message.
        :type message: str
        :param ignore_display: Whether to ignore display settings.
        :type ignore_display: bool, optional
        :param exec_info: Information about the exception, if any.
        :type exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]], optional
        :param stack_info: Whether to include stack information.
        :type stack_info: bool, optional
        :param stack_level: The level of stack information to include.
        :type stack_level: int, optional
        :return: None
        """
        if self.is_enabled_for(LogLevel.DEBUG):
            self._log(LogLevel.DEBUG, message, ignore_display, exec_info, stack_info, stack_level)

    def error(
            self,
            message: str,
            ignore_display: bool = False,
            exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]] = None,
            stack_info: bool = False,
            stack_level: int = 1
    ) -> None:
        """
        Logs a message with ERROR level.

        :param message: The log message.
        :type message: str
        :param ignore_display: Whether to ignore display settings.
        :type ignore_display: bool, optional
        :param exec_info: Information about the exception, if any.
        :type exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]], optional
        :param stack_info: Whether to include stack information.
        :type stack_info: bool, optional
        :param stack_level: The level of stack information to include.
        :type stack_level: int, optional
        :return: None
        """
        if self.is_enabled_for(LogLevel.ERROR):
            self._log(LogLevel.ERROR, message, ignore_display, exec_info, stack_info, stack_level)

    def find_caller(self, stack_info: bool = False, stack_level: int = 1) -> Tuple[CallerFrame, str]:
        """
        Finds the caller frame and optionally collects stack information.

        :param stack_info: Flag to collect stack information.
        :param stack_level: Maximum call stack depth to search.
        :return: Caller frame details and stack information.
        """
        if not isinstance(stack_info, bool):
            raise TypeError('stack_info should be a boolean.')
        elif not isinstance(stack_level, int):
            raise TypeError('stack_level should be an integer.')

        frame = inspect.currentframe()
        if frame is None:
            return CallerFrame(), ''

        while stack_level > 0:
            next_frame = frame.f_back
            if next_frame is None:
                break
            frame = next_frame
            if not self._is_internal_frame(frame):
                stack_level = -1

        caller_frame = CallerFrame.get_caller_details(frame)

        s_info = ''
        if stack_info:
            with io.StringIO() as s_io:
                s_io.write('Stack (most recent call last):\n')
                traceback.print_stack(frame, file=s_io)
                s_info = s_io.getvalue().rstrip('\n')

        return caller_frame, s_info

    def get_child(self, suffix: str) -> 'Logger':
        """
        Get a child logger with the specified suffix.

        :param suffix: The suffix to append to the logger's name.
        :type suffix: str
        :return: The child logger with the specified name.
        :rtype: Logger
        """
        if not isinstance(suffix, str):
            raise TypeError('suffix should be a string.')

        if self.root is not self:
            # Append the suffix to the logger's name if it's not the root logger
            suffix = '.'.join((self.name, suffix))

        return self.manager.get_logger(suffix)

    def get_effective_level(self) -> int:
        """
        Retrieves the effective log level for the logger.

        :return: The effective log level.
        :rtype: int
        """
        logger = self

        # Traverse through the logger and its ancestors
        while logger:
            # Check if the logger has a level set
            if logger.level:
                # Return the logger's level if set
                return logger.level
            # Move to the parent logger
            logger = logger.parent

        # Return INFO level if no level is set in the hierarchy
        return LogLevel.INFO

    def handle(self, record: Record, ignore_display: bool) -> None:
        """
        Handles the given log record by calling its handlers if the logger is not disabled.

        :param record: Log record to handle.
        :param ignore_display: Flag indicating whether to ignore display.
        :return: None
        """
        if not isinstance(record, Record):
            raise TypeError('record should be of Record type.')
        elif not isinstance(ignore_display, bool):
            raise TypeError('ignore_display should be a boolean.')

        if not self._disabled:
            self.call_handlers(record, ignore_display)

    def has_handlers(self) -> bool:
        """
        Checks if the logger or any of its ancestors have handlers.

        :return: True if the logger or any ancestor has handlers, False otherwise.
        :rtype: bool
        """
        caller = self
        while caller:
            if caller._handlers:
                return True
            if not caller._propagate:
                break
            else:
                caller = caller.parent
        return False

    def info(
            self,
            message: str,
            ignore_display: bool = False,
            exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]] = None,
            stack_info: bool = False,
            stack_level: int = 1
    ) -> None:
        """
        Logs a message with INFO level.

        :param message: The log message.
        :type message: str
        :param ignore_display: Whether to ignore display settings.
        :type ignore_display: bool, optional
        :param exec_info: Information about the exception, if any.
        :type exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]], optional
        :param stack_info: Whether to include stack information.
        :type stack_info: bool, optional
        :param stack_level: The level of stack information to include.
        :type stack_level: int, optional
        :return: None
        """
        if self.is_enabled_for(LogLevel.INFO):
            self._log(LogLevel.INFO, message, ignore_display, exec_info, stack_info, stack_level)

    def is_enabled_for(self, level: int) -> bool:
        """
        Checks if logging is enabled for the specified log level.

        :param level: The log level to check.
        :type level: int
        :return: True if logging is enabled for the specified level, False otherwise.
        :rtype: bool
        """
        if not isinstance(level, int):
            raise TypeError('level should be an integer.')

        if self._disabled:
            # Logging is disabled
            return False

        try:
            # Check the cache for the level's enabled status
            return self._cache[level]
        except KeyError:
            # Level not found in cache, calculate and cache the result
            self._acquire_lock()
            try:
                # Check if the manager's disable level is greater than or equal to the specified level
                if self.manager.disable >= level:
                    is_enabled = self._cache[level] = False  # Logging is disabled for this level
                else:
                    # Check if the effective level is greater than or equal to the specified level
                    is_enabled = self._cache[level] = (level >= self.get_effective_level())
            finally:
                self._release_lock()  # Release the lock

            return is_enabled

    def log(
            self,
            level: int,
            message: str,
            ignore_display: bool = False,
            exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]] = None,
            stack_info: bool = False,
            stack_level: int = 1
    ) -> None:
        """
        Logs a message at the specified level.

        :param level: The log level to use (DEBUG, INFO, ERROR, WARNING, CRITICAL).
        :type level: int
        :param message: The log message.
        :type message: str
        :param ignore_display: Whether to ignore display settings.
        :type ignore_display: bool, optional
        :param exec_info: Information about the exception, if any.
        :type exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]], optional
        :param stack_info: Whether to include stack information.
        :type stack_info: bool, optional
        :param stack_level: The level of stack information to include.
        :type stack_level: int, optional
        :return: None
        :raises TypeError: If the specified log level is not an integer.
        """
        if self.is_enabled_for(level):
            self._log(level, message, ignore_display, exec_info, stack_info, stack_level)

    @staticmethod
    def make_record(
            name: str,
            level: int,
            message: str,
            caller_frame: Optional[CallerFrame] = None,
            exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]] = None,
            stack_info: Optional[str] = None
    ) -> Record:
        """
        Creates a Record object with specified attributes.

        :param name: Logger name.
        :param level: Log level.
        :param message: Log message.
        :param caller_frame: Caller frame details.
        :param exec_info: Execution information.
        :param stack_info: Stack information.
        :return: Record object.
        """
        return Record(
            message=message,
            logger_name=name,
            level_number=level,
            caller_frame=caller_frame,
            exec_info=exec_info,
            stack_info=stack_info
        )

    def remove_handler(self, handler: Handler) -> None:
        """
        Removes a handler from the logger's list of handlers after acquiring the lock.

        :param handler: Handler object to remove.
        :return: None
        """
        if not issubclass(type(handler), Handler):
            raise TypeError('handler should be a subclass of Handler.')

        self._acquire_lock()
        try:
            if handler in self._handlers:
                self._handlers.remove(handler)
        finally:
            self._release_lock()

    def warning(
            self,
            message: str,
            ignore_display: bool = False,
            exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]] = None,
            stack_info: bool = False,
            stack_level: int = 1
    ) -> None:
        """
        Logs a message with WARNING level.

        :param message: The log message.
        :type message: str
        :param ignore_display: Whether to ignore display settings.
        :type ignore_display: bool, optional
        :param exec_info: Information about the exception, if any.
        :type exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]], optional
        :param stack_info: Whether to include stack information.
        :type stack_info: bool, optional
        :param stack_level: The level of stack information to include.
        :type stack_level: int, optional
        :return: None
        """
        if self.is_enabled_for(LogLevel.WARNING):
            self._log(LogLevel.WARNING, message, ignore_display, exec_info, stack_info, stack_level)


class Manager:
    """
    Manages loggers and their settings.
    """

    def __init__(self, root_node: Logger) -> None:
        """
        Initializes the Manager with a root logger.

        :param root_node: The root logger.
        :type root_node: Logger
        """
        if not isinstance(root_node, Logger):
            raise TypeError('root_node should be Logger type.')

        self._root = root_node
        self._disable = 0
        self._logger_dict = {}
        self._logger_class = None
        self._record_factory = None
        self._lock_name = None

    @property
    def disable(self) -> int:
        """
        Get the level at which logging is disabled.

        :return: The level at which logging is disabled.
        :rtype: int
        """
        return self._disable

    @disable.setter
    def disable(self, value: int) -> None:
        """
        Set the level at which logging is disabled.

        :param value: The level at which logging is disabled.
        :type value: int
        """
        if not isinstance(value, int):
            raise TypeError('disable should be an integer.')

        self._disable = value

    @property
    def lock_name(self) -> str:
        """
        Get the name of the lock used for thread safety.

        :return: The name of the lock.
        :rtype: str
        """
        return self._lock_name

    @lock_name.setter
    def lock_name(self, value: str) -> None:
        """
        Set the name of the lock used for thread safety.

        :param value: The name of the lock.
        :type value: str
        """
        if not isinstance(value, str):
            raise TypeError('lock_name should be a string.')

        self._lock_name = value

    @property
    def logger_class(self) -> Logger:
        """
        Get the logger class used for creating logger instances.

        :return: The logger class.
        :rtype: Logger
        """
        return self._logger_class

    @logger_class.setter
    def logger_class(self, value: Logger) -> None:
        """
        Set the logger class used for creating logger instances.

        :param value: The logger class.
        :type value: Logger
        """
        if not isinstance(value, Logger):
            raise TypeError('logger_class should be of Logger type.')

        self._logger_class = value

    @property
    def logger_dict(self) -> dict:
        """
        Get the dictionary mapping logger names to their instances.

        :return: The dictionary mapping logger names to their instances.
        :rtype: dict
        """
        return self._logger_dict

    @logger_dict.setter
    def logger_dict(self, value: dict) -> None:
        """
        Set the dictionary mapping logger names to their instances.

        :param value: The dictionary mapping logger names to their instances.
        :type value: dict
        """
        if not isinstance(value, dict):
            raise TypeError('logger_dict should be a dictionary.')

        self._logger_dict = value

    @property
    def record_factory(self) -> Record:
        """
        Get the factory used for creating log records.

        :return: The log record factory.
        :rtype: Record
        """
        return self._record_factory

    @record_factory.setter
    def record_factory(self, value: Record) -> None:
        """
        Set the factory used for creating log records.

        :param value: The log record factory.
        :type value: Record
        """
        if not isinstance(value, Record):
            raise TypeError('record_factory should be of Record type.')

        self._record_factory = value

    @property
    def root(self) -> Logger:
        """
        Get the root logger of the logging hierarchy.

        :return: The root logger.
        :rtype: Logger
        """
        return self._root

    @root.setter
    def root(self, value: Logger) -> None:
        """
        Set the root logger of the logging hierarchy.

        :param value: The root logger.
        :type value: Logger
        """
        if not isinstance(value, Logger):
            raise TypeError('root should be of Logger type.')

        self._root = value

    def _acquire_lock(self) -> None:
        """
        Private method to acquire a lock for thread safety.
        :return: None
        """
        self._lock_name = Lock.generate_name()
        self._create_lock()
        Lock.acquire(self._lock_name)

    def _create_lock(self) -> None:
        """
        Private method to create a lock.
        :return: None
        """
        Lock.create(self._lock_name)

    def _fix_up_children(self, registry: 'Registry', logger: Logger) -> None:
        """
        Fix up the children of the given registry and logger.
        This method ensures that the children's parent hierarchy is correctly set up.
        :param registry: The registry whose children need to be fixed up.
        :param logger: The logger to set as the parent for the children.
        :return: None
        """
        if not isinstance(registry, Registry):
            raise TypeError('registry should be of Registry type.')
        elif not isinstance(logger, Logger):
            raise TypeError('logger should be of Logger type.')

        # Get the name of the logger
        name = logger.name

        # Get the length of the logger name
        name_length = len(name)

        # Iterate through the keys (children) in the logger map of the registry
        for children in registry.logger_map.keys():
            # Check if the parent name of the children does not match the logger name
            if children.parent.name[:name_length] != name:
                # Set the parent of the logger to the parent of the children
                logger.parent = children.parent

                # Set the parent of the children to the logger
                children.parent = logger

    def _fix_up_parents(self, logger: Logger) -> None:
        """
        Fix up the parents of the given logger.
        This method ensures that the logger's parent hierarchy is correctly set up.
        :param logger: The logger whose parents need to be fixed up.
        :return: None
        """
        if not isinstance(logger, Logger):
            raise TypeError('logger should be of Logger type.')

        # Get the name of the logger
        name = logger.name

        # Find the last occurrence of '.' in the logger name
        index = name.rfind('.')

        # Initialize the return value
        return_value = None

        # Iterate until the index is greater than 0 and return_value is not set
        while (index > 0) and not return_value:
            # Get the substring of the logger name up to the current index
            substr = name[:index]

            # Check if the substring is not in the logger dictionary
            if substr not in self.logger_dict:
                # If not present, create a new Registry object and add it to the logger dictionary
                self.logger_dict[substr] = Registry(logger)
            else:
                # If present, get the object from the logger dictionary
                obj = self.logger_dict[substr]

                # Check if the object is an instance of Logger
                if isinstance(obj, Logger):
                    # If it is a Logger instance, set it as the return value
                    return_value = obj
                else:
                    # If it is a Registry instance, append the logger to it
                    assert isinstance(obj, Registry)
                    obj.append(logger)

            # Find the next occurrence of '.' in the logger name before the current index
            index = name.rfind('.', 0, index - 1)

        # If return_value is still not set, set it as the root logger
        if not return_value:
            return_value = self.root

        # Set the parent of the logger to the return value
        logger.parent = return_value

    def _release_lock(self) -> None:
        """
        Private method to release the lock acquired for thread safety.
        :return: None
        """
        Lock.release(self._lock_name)

    def clear_cache(self) -> None:
        """
        Clear the cache for all loggers and the root logger.
        This method acquires a lock for thread safety while clearing the cache.
        :return: None
        """
        # Acquire a lock for thread safety
        self._acquire_lock()
        try:
            # Clear the cache for all loggers in the logger dictionary
            for logger in self.logger_dict.values():
                if isinstance(logger, Logger):
                    logger.cache.clear()

            # Clear the cache for the root logger
            self.root.cache.clear()
        finally:
            # Release the lock after clearing the cache
            self._release_lock()

    def get_logger(self, name: str) -> Logger:
        """
        Retrieve a logger with the specified name.
        If the logger does not exist, it creates a new logger.
        This method acquires a lock for thread safety during logger retrieval and creation.
        :param name: Name of the logger
        :return: Logger instance
        """
        return_value = None

        # Validate input: name must be a string
        if not isinstance(name, str):
            raise TypeError('Logger name must be a string.')

        # Acquire a lock for thread safety
        self._acquire_lock()
        try:
            # Check if the logger already exists in the logger dictionary
            if name in self.logger_dict:
                return_value = self.logger_dict[name]

                # If the existing logger is a Registry, create a new logger and fix up parent and children relationships
                if isinstance(return_value, Registry):
                    registry = return_value
                    return_value = self.logger_class if self.logger_class else Logger(name)
                    return_value.manager = self
                    self.logger_dict[name] = return_value
                    self._fix_up_children(registry, return_value)
                    self._fix_up_parents(return_value)
            else:
                # If the existing logger is not a Registry, create a new logger and fix up parent relationship
                return_value = self.logger_class if self.logger_class else Logger(name)
                return_value.manager = self
                self.logger_dict[name] = return_value
                self._fix_up_parents(return_value)
        finally:
            # Release the lock after logger retrieval and creation
            self._release_lock()

        return return_value

    def set_logger(self, logger: Logger) -> None:
        """
        Set the logger class to be used for creating new loggers.
        The specified logger class must be a subclass of Logger.
        :param logger: Logger class or subclass
        :return: None
        """
        if not isinstance(logger, Logger):
            raise TypeError('logger should be of Logger type.')

        # Validate input: logger must be a subclass of Logger
        if logger != Logger:
            if not issubclass(type(logger), Logger):
                raise TypeError(f'logger "{logger.__name__}" not derived from pyloggermanager.Logger')

        # Set the logger class
        self.logger_class = logger


class Registry:
    """
    A registry to store and manage instances of Logger class.
    """

    def __init__(self, logger: Logger) -> None:
        """
        Initializes the LoggerRegistry with a single logger.

        :param logger: The initial logger to be stored in the registry.
        :type logger: Logger
        """
        if not isinstance(logger, Logger):
            raise TypeError('logger should be of Logger type.')

        self._logger_map = {
            logger: None
        }

    @property
    def logger_map(self) -> dict:
        """
        Get the dictionary mapping loggers to their associated values.

        :return: The dictionary mapping loggers to their associated values.
        :rtype: dict
        """
        return self._logger_map

    @logger_map.setter
    def logger_map(self, value: dict) -> None:
        """
        Set the dictionary mapping loggers to their associated values.

        :param value: The dictionary to set as the logger map.
        :type value: dict
        """
        if not isinstance(value, dict):
            raise TypeError('logger_map should be a dictionary.')

        self._logger_map = value

    def append(self, logger: Logger) -> None:
        """
        Add a new logger to the registry.

        :param logger: The logger to add to the registry.
        :type logger: Logger
        """
        if not isinstance(logger, Logger):
            raise TypeError('logger should be of Logger type.')

        if logger not in self.logger_map:
            self.logger_map[logger] = None


class RootLogger(Logger):
    """
    The RootLogger class represents the root logger in a logging hierarchy.
    It inherits from the Logger class and initializes itself with the name 'root' and the specified log level.
    The root logger serves as the ancestor of all other loggers in the logging hierarchy.
    """

    def __init__(self, level: int) -> None:
        """
        Constructs a new 'RootLogger' object with the specified log level.
        :param level: The log level for the root logger.
        :type level: int
        """
        super().__init__('root', level)


#########################################################################################################
# Below are configurations related to the pyloggermanager package.
# These settings and variables are not associated with any specific class or method.
# They establish default values and configurations for the pyloggermanager package.
# This section includes initialization of the logger class, root logger, manager instance, and lock name.
#########################################################################################################

# Default logger class used for creating new loggers
_logger_class = Logger(name='root')

# Default root logger with WARNING level
_root_logger = RootLogger(LogLevel.WARNING)

# Assign the root logger to the logger class
_logger_class.root = _root_logger

# Create a manager instance with the root logger
_logger_class.manager = Manager(_logger_class.root)

# Default lock name (empty string)
_lock_name = ''


def _acquire_lock() -> None:
    """
    Private method to acquire a lock for thread safety.

    :return: None
    """
    global _lock_name

    _lock_name = Lock.generate_name()
    _create_lock()
    Lock.acquire(_lock_name)


def _create_lock() -> None:
    """
    Private method to create a lock.

    :return: None
    """
    Lock.create(_lock_name)


def _release_lock() -> None:
    """
    Private method to release the lock acquired for thread safety.

    :return: None
    """
    Lock.release(_lock_name)


def _configure_handler(handler: Handler = None, formatter: Formatter = None) -> None:
    """
    This method configures the provided handler with the specified formatter if the handler does not already have one.

    :param handler: The handler to configure with a formatter if not already set.
    :type handler: Handler
    :param formatter: The formatter to set for the handler.
    :type formatter: Formatter
    :return: None
    """
    if handler:
        if not issubclass(type(handler), Handler):
            raise TypeError('handler should be a subclass of Handler class.')
    if formatter:
        if not issubclass(type(formatter), Formatter):
            raise TypeError('formatter should be a subclass of Formatter class.')

    if handler.formatter is None:
        handler.formatter = formatter


def _configure_root_logger_level(level: int) -> None:
    """
    This method configures the logging level for the root logger if the provided level is not None.

    :param level: The logging level to set for the root logger.
    :type level: int
    :return: None
    """
    if not isinstance(level, int):
        raise TypeError('level should be an integer.')

    if level is not None:
        _root_logger.level = level


def _create_default_handlers(
        file_name: str = None,
        file_mode: str = None,
        level: int = None,
        format_str: str = None,
        date_format: str = None,
        colorization=None,
        stream: Stream = None,
        encoding: str = None
) -> list:
    """
    This method creates and returns a list containing the default handler for logging,
    either a FileHandler if file_name is specified, or a StreamHandler if file_name is None.

    :param file_name: The name of the log file, if logging to a file.
    :type file_name: str
    :param file_mode: The file mode for opening the log file.
    :type file_mode: str
    :param level: The logging level for the handler.
    :type level: int
    :param format_str: The format string for formatting log messages.
    :type format_str: str
    :param date_format: The format string for formatting log message timestamps.
    :type date_format: str
    :param colorization: The colorization settings for log messages.
    :type colorization: pycolorecho.ColorMapper
    :param stream: The stream to log to, if not logging to a file.
    :type stream: Stream
    :param encoding: The encoding to use for the log file.
    :type encoding: str
    :return: A list containing the default handler configured based on the provided parameters.
    :rtype: list
    """
    from pycolorecho import ColorMapper

    if not isinstance(file_name, Union[str, NoneType]):
        raise TypeError('file_name should be a string.')
    elif not isinstance(file_mode, Union[str, NoneType]):
        raise TypeError('file_mode should be a string.')
    elif not isinstance(level, Union[int, NoneType]):
        raise TypeError('level should be an integer.')
    elif not isinstance(format_str, Union[str, NoneType]):
        raise TypeError('format_str should be a string.')
    elif not isinstance(date_format, Union[str, NoneType]):
        raise TypeError('date_format should be a string.')
    elif not isinstance(colorization, Union[ColorMapper, NoneType]):
        raise TypeError('colorization should be of Colorization type.')
    elif not isinstance(encoding, Union[str, NoneType]):
        raise TypeError('encoding should be a string.')

    if stream:
        if not issubclass(type(stream), Stream):
            raise TypeError('stream should be a subclass of Stream class.')

    if file_name:
        if 'b' not in file_mode:
            encoding = io.TextIOWrapper(io.BytesIO(), encoding=encoding).encoding

        handler = FileHandler(
            level=level,
            colorization=colorization,
            formatter=DefaultFormatter(format_str, date_format),
            file_name=file_name,
            file_mode=file_mode,
            encoding=encoding
        )
    else:
        handler = StreamHandler(stream=stream)

    return [handler]


def _validate_stream_and_file(handlers: list | None, stream: Stream = None, file_name: str = None) -> None:
    """
    Validate whether both stream and file_name are specified together when handlers are None.

    :param stream: The stream to write logs to.
    :type stream: Stream
    :param file_name: The name of the log file.
    :type file_name: str
    :param handlers: List of handlers.
    :type handlers: list
    :return: None
    """
    if not isinstance(handlers, Union[list, NoneType]):
        raise TypeError('handlers should be a list.')
    elif not isinstance(file_name, Union[str, NoneType]):
        raise TypeError('file_name should be a string.')

    if stream:
        if not issubclass(type(stream), Stream):
            raise TypeError('stream should be a subclass of Stream class.')

    if handlers is None:
        if stream is not None and file_name is not None:
            raise ValueError('stream and file_name should not be specified together.')
        elif stream is None and file_name is None:
            raise ValueError('At least handlers, stream, or file_name should be specified.')
    else:
        if stream is not None or file_name is not None:
            raise ValueError('stream or file_name should not be specified together with handlers.')


def load_config(
        file_name: str = 'default.log',
        file_mode: str = FileMode.APPEND,
        level: int = LogLevel.INFO,
        format_str: str = DEFAULT_FORMAT,
        date_format: str = DATE_FORMAT,
        stream: Stream = None,
        handlers: list = None,
        colorization=None,
        encoding: str = 'UTF-8'
) -> None:
    """
    This method loads the logging configuration based on the provided parameters.
    It acquires a lock for thread safety, configures default handlers if no handlers
    are specified, configures the formatter and level for each handler, and adds the
    handlers to the root logger. Finally, it releases the lock.

    :param file_name: The name of the log file, if logging to a file. Defaults to 'default.log'.
    :type file_name: str
    :param file_mode: The file mode for opening the log file. Defaults to FileMode.APPEND.
    :type file_mode: str
    :param level: The logging level for the handlers. Defaults to LogLevel.INFO.
    :type level: int
    :param format_str: The format string for formatting log messages. Defaults to DEFAULT_FORMAT.
    :type format_str: str
    :param date_format: The format string for formatting log message timestamps. Defaults to DATE_FORMAT.
    :type date_format: str
    :param stream: The stream to log to, if not logging to a file. Defaults to None.
    :type stream: Stream
    :param handlers: A list of handlers to configure. Defaults to None.
    :type handlers: list
    :param colorization: The colorization settings for log messages. Defaults to None.
    :type colorization: pycolorecho.ColorMapper
    :param encoding: The encoding to use for the log file. Defaults to 'UTF-8'.
    :type encoding: str
    :return: None
    """
    from pycolorecho import ColorMapper

    if not isinstance(file_name, Union[str, NoneType]):
        raise TypeError('file_name should be a string.')
    elif not isinstance(file_mode, Union[str, NoneType]):
        raise TypeError('file_mode should be a string.')
    elif not isinstance(level, int):
        raise TypeError('level should be an integer.')
    elif not isinstance(format_str, str):
        raise TypeError('format_str should be a string.')
    elif not isinstance(date_format, str):
        raise TypeError('date_format should be a string.')
    elif not isinstance(handlers, Union[list, NoneType]):
        raise TypeError('handlers should be a list.')
    elif not isinstance(colorization, Union[ColorMapper, NoneType]):
        raise TypeError('colorization should be of Colorization type.')
    elif not isinstance(encoding, Union[str, NoneType]):
        raise TypeError('encoding should be a string.')

    if stream:
        if not issubclass(type(stream), Stream):
            raise TypeError('stream should be a subclass of Stream class.')

    _acquire_lock()
    try:
        if not _root_logger.handlers:
            # if handlers is not None:
            _validate_stream_and_file(handlers, stream, file_name)

            if handlers is None:
                handlers = _create_default_handlers(
                    file_name, file_mode, level, format_str, date_format, colorization, stream, encoding
                )

            formatter = Formatter(format_str, date_format)
            for handler in handlers:
                _configure_handler(handler, formatter)
                _root_logger.add_handler(handler)

            if level is not None:
                _configure_root_logger_level(level)
    finally:
        _release_lock()


def get_logger(name: str = None) -> Logger:
    """
    Get a logger instance by name.

    :param name: The name of the logger.
    :type name: str
    :return: The logger instance.
    :rtype: Logger
    """
    if not name:
        return _root_logger
    elif isinstance(name, str) and name == _root_logger.name:
        return _root_logger
    else:
        return _logger_class.manager.get_logger(name)


def critical(
        message: str,
        ignore_display: bool = False,
        exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]] = None,
        stack_info: bool = False,
        stack_level: int = 1
) -> None:
    """
    Log a critical message.

    :param message: The message to be logged.
    :type message: str
    :param ignore_display: Whether to ignore display settings, defaults to False.
    :type ignore_display: bool, optional
    :param exec_info: Tuple containing exception information, defaults to None.
    :type exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]], optional
    :param stack_info: Whether to log stack information, defaults to False.
    :type stack_info: bool, optional
    :param stack_level: Level in the stack trace to show, defaults to 1.
    :type stack_level: int, optional
    """
    if len(_root_logger.handlers) == 0:
        load_config()
    _root_logger.critical(message, ignore_display, exec_info, stack_info, stack_level)


def debug(
        message: str,
        ignore_display: bool = False,
        exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]] = None,
        stack_info: bool = False,
        stack_level: int = 1
) -> None:
    """
    Log a debug message.

    :param message: The message to be logged.
    :type message: str
    :param ignore_display: Whether to ignore display settings, defaults to False.
    :type ignore_display: bool, optional
    :param exec_info: Tuple containing exception information, defaults to None.
    :type exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]], optional
    :param stack_info: Whether to log stack information, defaults to False.
    :type stack_info: bool, optional
    :param stack_level: Level in the stack trace to show, defaults to 1.
    :type stack_level: int, optional
    """
    if len(_root_logger.handlers) == 0:
        load_config()
    _root_logger.debug(message, ignore_display, exec_info, stack_info, stack_level)


def error(
        message: str,
        ignore_display: bool = False,
        exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]] = None,
        stack_info: bool = False,
        stack_level: int = 1
) -> None:
    """
    Log an error message.

    :param message: The message to be logged.
    :type message: str
    :param ignore_display: Whether to ignore display settings, defaults to False.
    :type ignore_display: bool, optional
    :param exec_info: Tuple containing exception information, defaults to None.
    :type exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]], optional
    :param stack_info: Whether to log stack information, defaults to False.
    :type stack_info: bool, optional
    :param stack_level: Level in the stack trace to show, defaults to 1.
    :type stack_level: int, optional
    """
    if len(_root_logger.handlers) == 0:
        load_config()
    _root_logger.error(message, ignore_display, exec_info, stack_info, stack_level)


def info(
        message: str,
        ignore_display: bool = False,
        exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]] = None,
        stack_info: bool = False,
        stack_level: int = 1
) -> None:
    """
    Log an informational message.

    :param message: The message to be logged.
    :type message: str
    :param ignore_display: Whether to ignore display settings, defaults to False.
    :type ignore_display: bool, optional
    :param exec_info: Tuple containing exception information, defaults to None.
    :type exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]], optional
    :param stack_info: Whether to log stack information, defaults to False.
    :type stack_info: bool, optional
    :param stack_level: Level in the stack trace to show, defaults to 1.
    :type stack_level: int, optional
    """
    if len(_root_logger.handlers) == 0:
        load_config()
    _root_logger.info(message, ignore_display, exec_info, stack_info, stack_level)


def warning(
        message: str,
        ignore_display: bool = False,
        exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]] = None,
        stack_info: bool = False,
        stack_level: int = 1
) -> None:
    """
    Log a warning message.

    :param message: The message to be logged.
    :type message: str
    :param ignore_display: Whether to ignore display settings, defaults to False.
    :type ignore_display: bool, optional
    :param exec_info: Tuple containing exception information, defaults to None.
    :type exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]], optional
    :param stack_info: Whether to log stack information, defaults to False.
    :type stack_info: bool, optional
    :param stack_level: Level in the stack trace to show, defaults to 1.
    :type stack_level: int, optional
    """
    if len(_root_logger.handlers) == 0:
        load_config()
    _root_logger.warning(message, ignore_display, exec_info, stack_info, stack_level)


def log(
        level: int,
        message: str,
        ignore_display: bool = False,
        exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]] = None,
        stack_info: bool = False,
        stack_level: int = 1
) -> None:
    """
    Log a message with the specified log level.

    :param level: The log level of the message.
    :type level: int
    :param message: The message to be logged.
    :type message: str
    :param ignore_display: Whether to ignore display settings, defaults to False.
    :type ignore_display: bool, optional
    :param exec_info: Tuple containing exception information, defaults to None.
    :type exec_info: Optional[Tuple[Type, BaseException, Optional[TracebackType]]], optional
    :param stack_info: Whether to log stack information, defaults to False.
    :type stack_info: bool, optional
    :param stack_level: Level in the stack trace to show, defaults to 1.
    :type stack_level: int, optional
    """
    if len(_root_logger.handlers) == 0:
        load_config()
    _root_logger.log(level, message, ignore_display, exec_info, stack_info, stack_level)


def disable(level: int = LogLevel.CRITICAL) -> None:
    """
    Disable logging up to the specified level.

    :param level: The log level up to which logging will be disabled, defaults to LogLevel.CRITICAL.
    :type level: int, optional
    """
    if not isinstance(level, int):
        raise TypeError('level should be an integer.')

    _root_logger.manager.disable = level
    _root_logger.manager.clear_cache()


def shutdown() -> None:
    """
    Shutdown all handlers by flushing and closing them.

    This function retrieves all handlers, flushes and closes them in reverse order to ensure proper shutdown,
    ignoring any errors that may occur during the process.
    """
    handlers = Handler.get_handlers()

    for handler in reversed(handlers[:]):
        try:
            if handler:
                try:
                    handler.flush()
                    handler.close()
                except (OSError, ValueError):
                    # Handle specific exceptions here if necessary
                    pass
        except BaseException:
            # Handle specific exceptions here if necessary
            pass

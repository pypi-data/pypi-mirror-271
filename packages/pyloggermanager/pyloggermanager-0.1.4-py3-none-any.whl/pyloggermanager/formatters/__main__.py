import io
import json
import time
import traceback
from types import TracebackType
from typing import Optional, Tuple, Type, Union

# The default format string used for log message formatting
DEFAULT_FORMAT = '%(time)s :: %(level_name)s :: %(message)s'
# The format string used for CSV log message formatting
CSV_FORMAT = '%(time)s,%(level_name)s,%(message)s'
# The format string used for JSON log message formatting
JSON_FORMAT = {
    "time": "%(time)s",
    "levelName": "%(level_name)s",
    "message": "%(message)s"
}

# The default date format string used for log message formatting
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


class Formatter:
    """
    Base class for log record formatters. Allows customization of log message format.
    Subclasses must implement the 'format' method to customize log message formatting.
    """

    def __init__(self, format_str: str | dict = DEFAULT_FORMAT, date_format: str = DATE_FORMAT) -> None:
        """
        Initialize the Formatter object

        :param format_str: The format string (or dict for JSON) used for log message formatting.
        :type format_str: str | dict
        :param date_format: The format string used for date and time formatting.
        :type date_format: str
        """
        if not isinstance(format_str, Union[str, dict]):
            raise TypeError('format_str should be either a string or dict.')
        elif not isinstance(date_format, str):
            raise TypeError('date_format should be a string.')

        self._format_str = format_str
        self._date_format = date_format

    @property
    def date_format(self) -> str:
        """
        Getter property for the date format used in log message formatting.

        :return: The date format string.
        :rtype: str
        """
        return self._date_format

    @date_format.setter
    def date_format(self, value: str) -> None:
        """
        Setter property for the date format used in log message formatting.

        :param value: The new date format string to set.
        :type value: str
        :return: None
        """
        if not isinstance(value, str):
            raise TypeError('date_format should be a string.')

        self._date_format = value

    @property
    def format_str(self) -> str | dict:
        """
        Getter property for the dict format used in log message formatting.

        :return: The dict format.
        :rtype: dict
        """
        return self._format_str

    @format_str.setter
    def format_str(self, value: str | dict) -> None:
        """
        Setter property for the dict format used in log message formatting.

        :param value: The new dict format to set.
        :type value: dict
        :return: None
        """
        if not isinstance(value, Union[str, dict]):
            raise TypeError('format_str should be either a string or dict.')

        self._format_str = value

    def format(self, record) -> str:
        """
        Formats the log record into a string based on the provided record object.

        :param record: The log record object containing log information.
        :type record: Record
        :return: The formatted log message as a string.
        :rtype: str
        """
        raise NotImplementedError('format() method must be implemented in subclasses.')

    @staticmethod
    def format_time(value: time.struct_time, date_format: str) -> str:
        """
        Formats the provided time value into a string using the specified date format.

        :param value: The time value to format.
        :type value: time.struct_time
        :param date_format: The date time format
        :type date_format: str
        :return: The formatted time string.
        :rtype: str
        """
        if not isinstance(value, time.struct_time):
            raise TypeError('value should be time.struct_time.')
        elif not isinstance(date_format, str):
            raise TypeError('date_format should be a string.')

        return time.strftime(date_format, value)

    @staticmethod
    def format_exception(
            exec_info: Optional[Tuple[Type[BaseException], BaseException, Optional[TracebackType]]] = None
    ) -> str:
        """
        Formats the exception information into a string.

        :param exec_info: Tuple containing exception information.
        :type exec_info: Optional[Tuple[Type[BaseException], BaseException, Optional[TracebackType]]]
        :return: The formatted exception string.
        :rtype: str
        """
        if exec_info:
            if isinstance(exec_info, Tuple) and \
                    len(exec_info) == 3 and \
                    isinstance(exec_info[0], type) and \
                    issubclass(exec_info[0], BaseException) and \
                    isinstance(exec_info[1], BaseException) and \
                    (exec_info[2] is None or isinstance(exec_info[2], TracebackType)):
                s_io = io.StringIO()
                traceback.print_exception(*exec_info, file=s_io)
                s = s_io.getvalue()
                s_io.close()
                return s.rstrip('\n')  # Remove trailing newline if present
            else:
                raise TypeError(
                    'exec_info should be of Tuple[Type[BaseException], BaseException, Optional[TracebackType]]'
                )
        else:
            return ''

    def _log_attributes(self, record, date_format: str) -> dict:
        """
        Extracts and organizes various attributes of a 'Record' object into a dictionary format.

        :param record: The log record object containing log information.
        :type record: Record
        :return: Dictionary format of log attributes.
        :rtype: dict
        """
        import pyloggermanager

        if not isinstance(record, pyloggermanager.Record):
            raise TypeError('record should be of Record type.')
        elif not isinstance(date_format, str):
            raise TypeError('date_format should be a string.')

        return {
            '%(time)s': self.format_time(record.time.timetuple(), date_format),
            '%(message)s': record.message,
            '%(logger_name)s': record.logger_name,
            '%(level_name)s': record.level_name,
            '%(level_number)d': record.level_number,
            '%(file_name)s': record.file_name,
            '%(class_name)s': record.class_name,
            '%(function_name)s': record.function_name,
            '%(module_name)s': record.module_name,
            '%(path_name)s': record.path_name,
            '%(exec_info)s': self.format_exception(record.exec_info),
            '%(stack_info)s': record.stack_info,
            '%(thread)d': record.thread,
            '%(thread_name)s': record.thread_name,
            '%(process_id)d': record.process_id
        }


class DefaultFormatter(Formatter):
    """
    Custom formatter for log records. Inherits from the 'Formatter' class.
    Allows customization of log record formatting using a specified format string.
    Replaces tokens in the format string with corresponding values from the log record.
    """

    def __init__(self, format_str: str = DEFAULT_FORMAT, date_format: str = DATE_FORMAT) -> None:
        """
        Initializes a 'DefaultFormatter' instance with the specified format string.

        :param format_str: Format string for log record formatting. Defaults to 'DEFAULT_FORMAT'.
        :type format_str: str
        """
        if not isinstance(format_str, str):
            raise TypeError('format_str should be a string.')

        super().__init__(format_str, date_format)

    def format(self, record) -> str:
        """
        Formats the given log record according to the format string.

        :param record: Log record to be formatted.
        :type record: Record
        :return: Formatted log message.
        :rtype: str
        """
        import pyloggermanager

        if not isinstance(record, pyloggermanager.Record):
            raise TypeError('record should be of Record type.')

        # Extracts log attributes in dictionary format
        log_attributes = super()._log_attributes(record, self.date_format)

        # Replaces tokens in the format string with corresponding log record values
        formatted_message = self.format_str
        for token, value in log_attributes.items():
            formatted_message = formatted_message.replace(token, str(value))

        return formatted_message


class CSVFormatter(Formatter):
    """
    Subclass of the 'Formatter' class for formatting log records in CSV format.
    Allows customization of the format string used for formatting log records.
    """

    def __init__(self, format_str: str = CSV_FORMAT, date_format: str = DATE_FORMAT) -> None:
        """
        Initializes a 'CSVFormatter' object with the specified format string.

        :param format_str: Format string defining the CSV format. Defaults to 'CSV_FORMAT'.
        :type format_str: str
        """
        if not isinstance(format_str, str):
            raise TypeError('format_str should be a string.')

        self._validate_format_str(format_str)
        super().__init__(format_str, date_format)

    def _validate_format_str(self, format_str: str) -> None:
        """
        Validates the format string to ensure it's a valid CSV format (separated by comma).

        :param format_str: Format string to validate.
        :type format_str: str
        :raises ValueError: If the format string is not a valid CSV format.
        """
        if not self._is_valid_csv_format(format_str):
            raise ValueError("Invalid CSV format string. Must be comma-separated.")

    @staticmethod
    def _is_valid_csv_format(format_str: str) -> bool:
        """
        Checks if the format string is a valid CSV format (separated by comma).

        :param format_str: Format string to check.
        :type format_str: str
        :return: True if the format string is a valid CSV format, False otherwise.
        :rtype: bool
        """
        return len(format_str.split(',')) >= 2

    def format(self, record) -> str:
        """
        Formats the given log record into a CSV string based on the specified format string.

        :param record: Log record.
        :type record: Record
        :return: Formatted CSV string representing the log record.
        :rtype: str
        """
        import pyloggermanager

        if not isinstance(record, pyloggermanager.Record):
            raise TypeError('record should be of Record type.')

        log_attributes = super()._log_attributes(record, self.date_format)
        formatted_values = []

        for token in self.format_str.split(','):
            if token in log_attributes:
                formatted_values.append(str(log_attributes[token]))
            else:
                formatted_values.append(token)  # Keep the original token if not found in log_attributes

        return ','.join(formatted_values)


class JSONFormatter(Formatter):
    """
    Subclass of the 'Formatter' class for formatting log records into JSON format.
    Provides methods to initialize the formatter with a custom format string,
    format log records into JSON strings, and handle JSON decoding errors.
    """

    def __init__(self, format_str: dict = None, date_format: str = DATE_FORMAT) -> None:
        """
        Initializes the JSONFormatter object with a custom format string.

        :param format_str: Custom dict format for JSON formatting. Defaults to 'JSON_FORMAT'.
        :type format_str: str
        """
        if format_str is None:
            format_str = JSON_FORMAT

        if not isinstance(format_str, dict):
            raise TypeError('format_str should be a dict.')

        self._validate_format_str(format_str)
        super().__init__(format_str, date_format)

    @staticmethod
    def _validate_format_str(format_str: dict) -> None:
        """
        Validates the format string to ensure it's a valid JSON format.

        :param format_str: Format string to validate.
        :type format_str: str
        :raises ValueError: If the format string is not a valid JSON format.
        """
        try:
            json.dumps(format_str)
        except ValueError:
            raise ValueError("Invalid JSON format string.")

    def format(self, record) -> str:
        """
        Formats the given log record into a JSON string.

        :param record: Log record.
        :type record: Record
        :return: JSON-formatted string representing the log record attributes.
        :rtype: str
        """
        import pyloggermanager

        if not isinstance(record, pyloggermanager.Record):
            raise TypeError('record should be of Record type.')

        log_attributes = super()._log_attributes(record, self.date_format)
        format_dict = self.format_str  # No need to convert format_str to JSON; it's already a dictionary

        formatted_values = {}
        for key, value in format_dict.items():
            if isinstance(value, list):
                formatted_items = []
                for item in value:
                    if isinstance(item, dict):
                        formatted_item = {}
                        for k1, v1 in item.items():
                            formatted_item[k1] = str(log_attributes.get(v1, v1))
                        formatted_items.append(formatted_item)
                    else:
                        formatted_items.append(str(log_attributes.get(item, item)))
                formatted_values[key] = formatted_items
            else:
                formatted_values[key] = str(log_attributes.get(value, value))

        return json.dumps(formatted_values, indent=4)

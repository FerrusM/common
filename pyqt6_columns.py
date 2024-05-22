import typing
from PyQt6 import QtCore, QtGui

DEFAULT_VALUE = QtCore.QVariant()  # Значение по умолчанию.


class Column:
    """Класс столбца."""
    def __init__(self, data_function=None, display_function=None, tooltip_function=None,
                 background_function=None, foreground_function=None):
        self.getData = data_function  # Функция для получения данных.
        self.getDisplay = data_function if display_function is None else display_function  # Функция для отображения данных.
        self.getToolTip = tooltip_function  # Функция для получения подсказки к отображаемым данным.
        self.getBackground = background_function
        self.getForeground = foreground_function

    def __call__(self, role: int, *args, **kwargs) -> typing.Any:
        match role:
            case QtCore.Qt.ItemDataRole.UserRole:
                return DEFAULT_VALUE if self.getData is None else self.getData(*args, **kwargs)
            case QtCore.Qt.ItemDataRole.DisplayRole:
                return DEFAULT_VALUE if self.getDisplay is None else self.getDisplay(*args, **kwargs)
            case QtCore.Qt.ItemDataRole.ToolTipRole:
                return DEFAULT_VALUE if self.getToolTip is None else self.getToolTip(*args, **kwargs)
            case QtCore.Qt.ItemDataRole.BackgroundRole:
                return DEFAULT_VALUE if self.getBackground is None else self.getBackground(*args, **kwargs)
            case QtCore.Qt.ItemDataRole.ForegroundRole:
                return DEFAULT_VALUE if self.getForeground is None else self.getForeground(*args, **kwargs)
            case _:
                return DEFAULT_VALUE


class Header:
    """Класс заголовка."""
    def __init__(self, title: str | None = None, tooltip: str | None = None, text_color: QtGui.QBrush | None = None):
        self.__title: str | None = title  # Название столбца.
        self.__tooltip: str | None = tooltip  # Подсказка в заголовке.
        self.__text_color: QtGui.QBrush | None = text_color  # Цвет текста.

    def __call__(self, role: int) -> typing.Any:
        match role:
            case QtCore.Qt.ItemDataRole.DisplayRole:
                return DEFAULT_VALUE if self.__title is None else self.__title
            case QtCore.Qt.ItemDataRole.ToolTipRole:
                return DEFAULT_VALUE if self.__tooltip is None else self.__tooltip
            case QtCore.Qt.ItemDataRole.ForegroundRole:
                return DEFAULT_VALUE if self.__text_color is None else self.__text_color
            case _:
                return DEFAULT_VALUE


class ColumnWithHeader(Column):
    def __init__(self, data_function=None, display_function=None, tooltip_function=None,
                 background_function=None, foreground_function=None,
                 header: Header | None = None):
        super().__init__(data_function, display_function, tooltip_function, background_function, foreground_function)
        self.__header: Header | None = header

    def header(self, role: int = ...) -> typing.Any:
        return DEFAULT_VALUE if self.__header is None else self.__header(role=role)

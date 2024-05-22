from PyQt6 import QtCore, QtWidgets, QtGui

TITLE_FONT = QtGui.QFont()
TITLE_FONT.setPointSize(9)
TITLE_FONT.setBold(True)


class TitleLabel(QtWidgets.QLabel):
    """Класс QLabel'а-заголовка."""
    def __init__(self, text: str, parent: QtWidgets.QWidget | None = None):
        super().__init__(text=text, parent=parent)
        self.setFont(TITLE_FONT)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)


class TitleWithCount(QtWidgets.QHBoxLayout):
    """Виджет, представляющий собой отцентрированный заголовок с QLabel'ом количества чего-либо в правом углу."""
    def __init__(self, title: str, count_text: str = '0', parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.setSpacing(0)

        self.addSpacing(10)
        self.addStretch(1)
        self.addWidget(TitleLabel(text=title, parent=parent), 0)

        self.__label_count = QtWidgets.QLabel(text=count_text, parent=parent)
        self.__label_count.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.addWidget(self.__label_count, 1)

        self.addSpacing(10)

    def setCount(self, count_text: str | None):
        self.__label_count.setText(count_text)

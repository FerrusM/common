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


class TableViewPanel(QtWidgets.QGroupBox):
    def __init__(self, title: str, model: QtCore.QAbstractItemModel | None = None, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent=parent)

        verticalLayout_main = QtWidgets.QVBoxLayout(self)
        verticalLayout_main.setContentsMargins(2, 2, 2, 2)
        verticalLayout_main.setSpacing(2)

        self.titlebar = TitleWithCount(title=title, count_text='0', parent=self)
        verticalLayout_main.addLayout(self.titlebar, 0)

        self.tableView = QtWidgets.QTableView(parent=self)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableView.setSortingEnabled(True)
        verticalLayout_main.addWidget(self.tableView, 1)

        self.__model_reset_connection: QtCore.QMetaObject.Connection = QtCore.QMetaObject.Connection()
        self.__rows_inserted_connection: QtCore.QMetaObject.Connection = QtCore.QMetaObject.Connection()
        self.__data_changed_connection: QtCore.QMetaObject.Connection = QtCore.QMetaObject.Connection()

        self.setModel(model)

    def setModel(self, model: QtCore.QAbstractItemModel | None):
        old_model: QtCore.QAbstractItemModel | None = self.tableView.model()
        if old_model is not None:
            model_reset_disconnect_flag: bool = old_model.disconnect(self.__model_reset_connection)
            rows_inserted_disconnect_flag: bool = old_model.disconnect(self.__rows_inserted_connection)
            data_changed_disconnect_flag: bool = old_model.disconnect(self.__data_changed_connection)
            assert model_reset_disconnect_flag and rows_inserted_disconnect_flag and data_changed_disconnect_flag, 'Не удалось отключить слот!'

        self.tableView.setModel(model)  # Подключаем модель к таблице.

        if model is not None:
            def __onModelUpdated():
                """Выполняется при изменении модели."""
                self.titlebar.setCount(str(model.rowCount()))
                self.tableView.resizeColumnsToContents()  # Авторазмер столбцов под содержимое.

            __onModelUpdated()
            self.__model_reset_connection = model.modelReset.connect(__onModelUpdated)
            self.__rows_inserted_connection = model.rowsInserted.connect(lambda prnt, first, last: __onModelUpdated())
            self.__data_changed_connection = model.dataChanged.connect(lambda topLeft, bottomRight, roles: __onModelUpdated())

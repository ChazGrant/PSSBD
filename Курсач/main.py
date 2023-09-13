"""
Программный продукт может быть:

    законченным самостоятельным приложением;

    модулем или пакетом расширения, подключаемым к поддерживающему 
    его приложению;

    процедурой или набором процедур (функций) в составе законченного 
    приложения;

    законченным программным кодом на интерпретируемом языке 
    программирования, поддерживаемом некоторым приложением.

    СУД должна работать с несколькими ролями: администратор, 
    пользователь, суперпользователь

    СУД должна обеспечивать многопользовательский режим

    СУД должна обеспечивать защиту на уровне строк (RLS) 

    СУД должна обеспечивать различный и в то же время полный клиентский 
    интерфейс в зависимости от роли.
"""



# Оператор скорой помощи (имеет доступ ко всем таблицам. Добавление,
# удаление заявок на вызов скорой помощи, добавление больных)

# Врач
# (имеет доступ к таблицам заявок, больные. Может только
# просматривать таблицу заявок, просматривать, удалять больных)

# Медсестра (имеет доступ только к таблице больные. Может только
# просматривать таблицу больные)


from typing import List
from PyQt5 import QtGui, QtWidgets, QtCore
from main_formUI import Ui_MainWindow
import psycopg2

from inspect import getmembers, isfunction
import requests

QUERIES = dict()
for function_name, function in getmembers(requests, isfunction):
    QUERIES[function_name] = function

def showMessage(text: str):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(text)
    msg.setWindowTitle("Info")
    msg.exec_()

def showError(text: str):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(text)
    msg.setWindowTitle("Info")
    msg.exec_()

TABLES_DICT = {
    "Больные": "sick_people",
    "Заявки на вызов": "call_requests",
    "Причины вызова": "call_reason",
    "Станции скорой помощи": "first_aid_stations",
    "Процедуры": "procedure",
    "Заявки на процедуры": "procedure_application",
    "Социальные статусы": "social_status"
}


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    window_closed = QtCore.pyqtSignal()
    def __init__(self, cursor, conn):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.__setComboBoxes()
        self._cursor = cursor
        self._conn = conn

        self._new_rows_added = list()

        self.visualiseTable_pushButton.pressed.connect(self._visualizeTable)
        self.visualizeQuery_pushButton.pressed.connect(self._visualizeQuery)

        self.addRow_pushButton.pressed.connect(self._addRowToTheTableWidget)
        self.addRecord_pushButton.pressed.connect(self._addRecord)

        self.deleteRecord_pushButton.pressed.connect(self._deleteRecord)

    def __setComboBoxes(self):
        self.__setTables()
        self.__setQueries()

    def __setTables(self):
        for table in TABLES_DICT.keys():
            self.tables_comboBox.addItem(table)

    def __setQueries(self):
        for query in QUERIES.keys():
            self.queries_comboBox.addItem(query)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.window_closed.emit()
        return super().closeEvent(a0)

    def _addRowToTheTableWidget(self):
        current_row_amount = self.tableWidget.rowCount()
        if current_row_amount == 0:
            return
        
        self.tableWidget.setRowCount(current_row_amount + 1)
        self._new_rows_added.append(current_row_amount + 1)

    def _addRecord(self):
        columns_names = []
        table_name = TABLES_DICT[self.tables_comboBox.currentText()]
        for column in range(self.tableWidget.columnCount()):
            columns_names.append(self.tableWidget.horizontalHeaderItem(column).\
                                 text())

        from datetime import datetime
        for row_idx in self._new_rows_added:
            row = []
            for column_idx in range(1, self.tableWidget.columnCount()):
                error_occured = False
                try:
                    _item_value = self.tableWidget.item(row_idx - 1, column_idx).text()
                    try:
                        _item_value = datetime.strptime(_item_value, "%Y-%m-%d")
                        print(_item_value)
                    except ValueError:
                        pass
                    row.append(_item_value)
                except AttributeError:
                    error_occured = True
                    break

            if error_occured:
                continue

            table_columns = ", ".join(columns_names[1:])
            table_values = ", ".join([f"'{value}'" for value in row])
            try:
                query = "INSERT INTO %s(%s) VALUES (%s)" % (table_name, table_columns, table_values)
                self._cursor.execute(query)
            except psycopg2.errors.InvalidDatetimeFormat:
                self._conn.rollback()
                showError("Неверный формат даты\nПример правильного формата: 2001-01-30")
                return
            self._cursor.execute(query)
            self._conn.rollback()
            print(query)

    def _visualizeTable(self):
        try:
            self._cursor.execute("SELECT * FROM %s" % TABLES_DICT[self.tables_comboBox.currentText()])
        except psycopg2.errors.InsufficientPrivilege:
            showError("У Вас недостаточно прав для работы с данной таблицей")
            self._conn.rollback()
            return
        
        columns_names = [desc[0] for desc in self._cursor.description]
        self._fillData(columns_names)

    def _visualizeQuery(self):
        query_name = self.queries_comboBox.currentText()
        try:
            QUERIES[query_name](self._cursor)
        except psycopg2.errors.InsufficientPrivilege:
            showError("У Вас недостаточно прав для выполнения данного запроса")
            self._conn.rollback()
            return
        
        columns_names = [desc[0] for desc in self._cursor.description]
        self._fillData(columns_names)

    def _fillData(self, columns_names: List[str]):
        columns_amount = len(columns_names)
        
        self.tableWidget.setColumnCount(columns_amount)
        self.tableWidget.setHorizontalHeaderLabels(columns_names)

        data = self._cursor.fetchall()
        self.tableWidget.setRowCount(len(data))
        for row_idx, row in enumerate(data):
            for column_idx, item in enumerate(row):
                _item = QtWidgets.QTableWidgetItem(str(item))
                _item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(row_idx, column_idx, _item)

        self.tableWidget.resizeColumnsToContents()

    def _deleteRecord(self):
        current_table = TABLES_DICT[self.tables_comboBox.currentText()]
        selected_row = self.tableWidget.currentRow()
        unique_idx = self.tableWidget.item(selected_row, 0).text()
        
        self._cursor.execute("SELECT * FROM %s LIMIT 0" % (current_table, ))
        column_name = self._cursor.description[0][0]

        query = "DELETE FROM %s WHERE %s = %s" % (current_table, column_name, unique_idx)

        try:
            self._cursor.execute(query)
            self._conn.rollback()
        except psycopg2.errors.InsufficientPrivilege:
            showError("У Вас недостаточно прав для удаленя данных")
            self._conn.rollback()
            return


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    widget.show()
    app.exec_()

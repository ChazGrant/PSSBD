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


from typing import List, Any, Union
from PyQt5 import QtGui, QtWidgets, QtCore
from main_formUI import Ui_MainWindow
import psycopg2

from inspect import getmembers, isfunction
import sys

from numpy import round as np_round
import matplotlib.pyplot as plt

import openpyxl
import datetime


if "--test" in sys.argv:
    TESTING_ENABLED = 1
    requests, complex_requests = [], []
else:
    TESTING_ENABLED = 0
    import complex_requests, requests


QUERIES = dict()
for function_name, function in getmembers(requests, isfunction):
    QUERIES[function_name] = function

for function_name, function in getmembers(complex_requests, isfunction):
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

def drawPieChart(values: List[int], labels: List[str], title: str) -> Union[str, None]:
    if not len(values) == len(labels):
        return "Значения и метки должны быть одинаковой длины"

    max_index_value = values.index(max(values))
    get_value = lambda x: np_round(x / 100 * sum(values))
    plt.pie(values, labels=labels, explode=tuple([0 for _ in values[:max_index_value]]) + tuple([.1]) + tuple([0 for _ in values[max_index_value + 1:]]), autopct=get_value)
    plt.title(title)
    plt.show()

def saveDataToExcel(columns_names: List[str], values: List[List[Any]], report_name: str) -> None:
    wb = openpyxl.Workbook()
    ws = wb.active

    for idx, column in enumerate(columns_names):
        ws.cell(row=1, column=idx + 1).value = column
        ws.cell(row=1, column=idx + 1).font = openpyxl.styles.Font(bold=True)

    for row_idx, row in enumerate(values):
        for column_idx, column in enumerate(row):
            ws.cell(row=row_idx + 2, column=column_idx + 1).value = column

    current_datetime = datetime.datetime.now().strftime("%d%m%y%H%M%S")
    wb_name = f"Отчёт по {report_name} {current_datetime}.xlsx"
    wb.save(wb_name)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    window_closed = QtCore.pyqtSignal()
    def __init__(self, cursor, conn):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.__setComboBoxes()
        self._cursor = cursor 
        self._conn = conn

        self._new_rows_added = list()

        self.visualizeTable_pushButton.pressed.connect(self._visualizeTable)
        self.visualizeQuery_pushButton.pressed.connect(self._visualizeQuery)
        self.saveToExcel_pushButton.pressed.connect(self._saveToExcel)
        self.buildSummaryChart_pushButton.pressed.connect(self._buildSummaryChart)
        self.findByCriteria_pushButton.pressed.connect(self._visualizeTable)

        self.buildSummaryChart_pushButton.setEnabled(False)

        self.addRow_pushButton.pressed.connect(self._addRowToTheTableWidget)
        self.addRecord_pushButton.pressed.connect(self._addRecord)

        self.tables_comboBox.currentTextChanged.connect(self._tablesChangedEvent)
        self.queries_comboBox.currentTextChanged.connect(self.__clearTableWidget)
        
        self.enableSorting_checkBox.stateChanged.connect(self._updateSortingButtonsState)

        self.deleteRecord_pushButton.pressed.connect(self._deleteRecord)

        self.__fillColumns()

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

    def __clearTableWidget(self):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)

    def _tablesChangedEvent(self):
        self.__fillColumns()
        self.__clearTableWidget()

    @property
    def _selectedColumn(self) -> str:
        return self.columns_comboBox.currentText()

    @property
    def _selectedTable(self) -> str:
        return TABLES_DICT[self.tables_comboBox.currentText()]

    @property
    def _criteriaPart(self) -> str:
        if len(self.columnCriteria_textEdit.toPlainText()):
            criteria_part = "WHERE {} = '{}' ".format(self._selectedColumn,\
                                                     self.columnCriteria_textEdit.toPlainText())
            return criteria_part
        
        return ""

    @property
    def _sortingPart(self) -> str:
        sorting_part = ""
        if self.enableSorting_checkBox.isChecked():
            sorting_part = "ORDER BY " + self._selectedColumn
            if self.sortByAscending_radioButton.isChecked():
                sorting_part += " ASC"
            else:
                sorting_part += " DESC"

        return sorting_part

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

    def _visualizeTable(self):
        if self.buildSummaryChart_pushButton.isEnabled():
            self.buildSummaryChart_pushButton.setEnabled(False)

        try:
            self._cursor.execute("SELECT * FROM %s %s %s" % (self._selectedTable, \
                self._criteriaPart, self._sortingPart))
        except psycopg2.errors.InsufficientPrivilege:
            showError("У Вас недостаточно прав для работы с данной таблицей")
            self._conn.rollback()
            return
        except psycopg2.errors.InvalidTextRepresentation:
            showError("Ошибка в формате данных")
            self._conn.rollback()
            return
        
        columns_names = [desc[0] for desc in self._cursor.description]
        self.__fillData(columns_names)

    def _visualizeQuery(self):
        query_name = self.queries_comboBox.currentText()
        if "total" in query_name.lower():
            self.buildSummaryChart_pushButton.setEnabled(True)
        else:
            self.buildSummaryChart_pushButton.setEnabled(False)
            
        try:
            QUERIES[query_name](self._cursor)
        except psycopg2.errors.InsufficientPrivilege:
            showError("У Вас недостаточно прав для выполнения данного запроса")
            self._conn.rollback()
            return
        
        columns_names = [desc[0] for desc in self._cursor.description]
        self.__fillData(columns_names)

    def _updateSortingButtonsState(self):
        self.sortByAscending_radioButton.setEnabled(self.enableSorting_checkBox.isChecked())
        self.sortByDescending_radioButton.setEnabled(self.enableSorting_checkBox.isChecked())

    def __fillColumns(self) -> None:
        selected_table = TABLES_DICT[self.tables_comboBox.currentText()]
        self._cursor.execute("SELECT * FROM %s LIMIT 0;" % selected_table)
        columns_names = [desc[0] for desc in self._cursor.description]
        
        self.columns_comboBox.clear()
        for column_name in columns_names:
            self.columns_comboBox.addItem(column_name)

    def __fillData(self, columns_names: List[str]):
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

    def _saveToExcel(self):
        if self.tableWidget.rowCount() == 0:
            return

        columns_values = [self.tableWidget.horizontalHeaderItem(column).text() for column in range(self.tableWidget.columnCount())]
        values: List[List[Any]] = []
        
        for row in range(self.tableWidget.rowCount()):
            _inner_values: List[Any] = []
            for column in range(self.tableWidget.columnCount()):
                _inner_values.append(self.tableWidget.item(row, column))

            values.append(_inner_values)

        saveDataToExcel(columns_values, values, self.queries_comboBox.currentText())

    def _buildSummaryChart(self):
        if self.tableWidget.rowCount() == 0:
            return

        values, labels = [], []
        if self.tableWidget.columnCount() > 1:
            for row in range(self.tableWidget.rowCount()):
                labels.append(self.tableWidget.item(row, 0).text())
                values.append(int(self.tableWidget.item(row, 1).text()))
        else:
            for column in range(self.tableWidget.columnCount()):
                try:
                    labels.append(self.tableWidget.horizontalHeaderItem(column).text())
                    values.append(int(self.tableWidget.item(0, column).text()))
                except ValueError:
                    labels.pop()

        drawPieChart(values, labels, self.queries_comboBox.currentText())

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
    if TESTING_ENABLED:
        widget = MainWindow([], [])
    else:
        widget = MainWindow()
    widget.show()
    app.exec_()

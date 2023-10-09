from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from compoundForm_formUI import Ui_Form
import psycopg2

from typing import List, Any, Dict


def showError(text: str):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(text)
    msg.setWindowTitle("Info")
    msg.exec_()


class CompoundForm(QtWidgets.QMainWindow, Ui_Form):
    first_choice_selected, second_choice_selected = pyqtSignal(), pyqtSignal() 
    def __init__(self,
                main_table_name: str,
                main_table_columns_names: List[str], 
                main_table_columns_values: List[Any], 
                child_table_names: List[str],
                child_table_columns_names: List[List[str]], 
                child_tables_column_values: List[Any],
                cursor,
                conn):
        super(CompoundForm, self).__init__()
        self.setupUi(self)

        self._cursor: psycopg2.cursor = cursor
        self._conn: psycopg2.connection = conn
        self._main_table_name = main_table_name

        self._new_rows_added: List[List[int]] = [[], []]
        self._updatedRecordsInfo: List[Dict[int, Dict[str, str]]] = [
            {0: {}}, 
            {1: {}}
        ]
        
        self.childTables_comboBox.currentTextChanged.connect(self._fillChildTable)

        self.addRowToMainTable_pushButton.pressed.connect(lambda: self._addRow(True))
        self.addRowToChildTable_pushButton.pressed.connect(lambda: self._addRow(False))
        self.addRecord_pushButton.pressed.connect(self._addRecord)
        self.updateRecord_pushButton.pressed.connect(self._updateRecord)
        self.deleteRecord_pushButton.pressed.connect(self._deleteRecord)

        self._child_table_names = child_table_names
        self._child_tables_column_values = child_tables_column_values
        self._child_tables_columns_names = child_table_columns_names

        for child_table_name in child_table_names:
            self.childTables_comboBox.addItem(child_table_name)

        self._fillMainTable(main_table_columns_names, main_table_columns_values)

    @property
    def _getTablesWidgets(self) -> List[QtWidgets.QTableWidget]:
        return [self.mainTable_tableWidget, self.childTable_tableWidget]

    def _addRow(self, is_main_table: bool) -> None:
        if is_main_table:
            next_row_count = self.mainTable_tableWidget.rowCount() + 1
            self.mainTable_tableWidget.setRowCount(next_row_count)
            self._new_rows_added[0].append(next_row_count)
        else:
            next_row_count = self.childTable_tableWidget.rowCount() + 1
            self.childTable_tableWidget.setRowCount(next_row_count)
            self._new_rows_added[1].append(next_row_count)

    def _addRecord(self):
        self._addRecordToTheMainTable()
        self._addRecordToTheChildTable()

    def _addRecordToTheMainTable(self):
        new_rows_added = self._new_rows_added[0]

        columns_names = []
        table_name = self._main_table_name
        for column in range(self.mainTable_tableWidget.columnCount()):
            columns_names.append(self.mainTable_tableWidget.horizontalHeaderItem(column).text())

        from datetime import datetime
        for row_idx in new_rows_added:
            row = []
            for column_idx in range(1, self.mainTable_tableWidget.columnCount()):
                error_occured = False
                try:
                    _item_value = self.mainTable_tableWidget.item(row_idx - 1, column_idx).text()
                    try:
                        _item_value = datetime.strptime(_item_value, "%Y-%m-%d")
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
                return showError("Неверный формат даты\nПример правильного формата: 2001-01-30")

            self._cursor.execute(query)
            self._conn.rollback()

    def _addRecordToTheChildTable(self):
        new_rows_added = self._new_rows_added[1]

        columns_names = []
        table_name = self._main_table_name
        for column in range(self.childTable_tableWidget.columnCount()):
            columns_names.append(self.childTable_tableWidget.horizontalHeaderItem(column).text())

        from datetime import datetime
        for row_idx in new_rows_added:
            row = []
            for column_idx in range(1, self.childTable_tableWidget.columnCount()):
                error_occured = False
                try:
                    _item_value = self.childTable_tableWidget.item(row_idx - 1, column_idx).text()
                    try:
                        _item_value = datetime.strptime(_item_value, "%Y-%m-%d")
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
                return showError("Неверный формат даты\nПример правильного формата: 2001-01-30")

            self._cursor.execute(query)
            self._conn.rollback()

    def _addChildCellToArray(self):
        self._addCellToAray(self.childTable_tableWidget, 0)
    
    def _addMainCellToArray(self):
        self._addCellToAray(self.mainTable_tableWidget, 1)

    def _addCellToAray(self, table_widget: QtWidgets.QTableWidget, table_idx: int):
        selected_item = table_widget.selectedItems()[0]
        new_value = selected_item.text()

        seleted_row = table_widget.row(selected_item)
        seleted_column = table_widget.column(selected_item)

        selected_column_name = table_widget.horizontalHeaderItem(seleted_column).text()
        idx_column_value = table_widget.item(seleted_row, 0).text()
        
        if idx_column_value not in self._updatedRecordsInfo[table_idx].keys():
            self._updatedRecordsInfo[table_idx][idx_column_value] = {selected_column_name: new_value}
        else:
            self._updatedRecordsInfo[table_idx][idx_column_value][selected_column_name] = new_value

    def _updateRecord(self):
        queries = []
        tables_widget = [self.mainTable_tableWidget, self.childTable_tableWidget]
        tables_names = [self._main_table_name, self.childTables_comboBox.currentText()]

        for table_idx, update_info in enumerate(self._updatedRecordsInfo):
            table_name = tables_names[table_idx]
            for main_column_idx, items_dict in update_info.items():
                main_column_name = tables_widget[table_idx].horizontalHeaderItem(0).text()
                new_columns_values = []
                for column_name, new_value in items_dict.items():
                    new_columns_values.append("{} = '{}'".format(column_name, new_value))

                query = "UPDATE TABLE {} SET {} WHERE {} = {}".format(table_name, 
                            ", ".join(item for item in new_columns_values),
                            main_column_name,
                            main_column_idx)
                queries.append(query)

        for query in queries:
            try:
                self._cursor.execute(query)
            except Exception as e:
                showError(str(e))
                self._conn.rollback()

    def _deleteRecord(self) -> None:
        current_tables = [self._main_table_name, self.childTables_comboBox.currentText()]
        main_columns = [self.mainTable_tableWidget.horizontalHeaderItem(0).text(),
                        self.childTable_tableWidget.horizontalHeaderItem(0).text()]
        for idx, table_widget in enumerate(self._getTablesWidgets):
            selected_row = table_widget.currentRow()
            unique_idx = table_widget.item(selected_row, 0).text()
            
            column_name = main_columns[idx]
            query = "DELETE FROM %s WHERE %s = %s" % (current_tables[idx], column_name, unique_idx)

            try:
                self._cursor.execute(query)
                self._conn.rollback()
            except psycopg2.errors.InsufficientPrivilege:
                showError("У Вас недостаточно прав для удаленя данных")
                self._conn.rollback()
                return

    def _fillChildTable(self) -> None:
        try:
            self.childTable_tableWidget.cellChanged.disconnect(self._addChildCellToArray)
        except TypeError:
            pass
        selected_child_table = self.childTables_comboBox.currentText()
        child_table_idx = self._child_table_names.index(selected_child_table)

        child_table_columns_names = self._child_tables_columns_names[child_table_idx]
        child_table_values = self._child_tables_column_values[child_table_idx]
        
        self.mainTable_tableWidget.setRowCount(len(child_table_values))
        self.mainTable_tableWidget.setColumnCount(len(child_table_columns_names))

        self.mainTable_tableWidget.setHorizontalHeaderLabels(child_table_columns_names)
        for row_idx, items in enumerate(child_table_values):
            for column_idx, item in enumerate(items):
                _item = QtWidgets.QTableWidgetItem(item)
                self.childTable_tableWidget.setItem(row_idx, column_idx, _item)

        self.childTable_tableWidget.cellChanged.connect(self._addChildCellToArray)

    def _fillMainTable(self, 
                       main_table_columns_names: List[str],
                       main_table_columns_values: List[Any]) -> None:
        self.mainTable_tableWidget.setRowCount(len(main_table_columns_values))
        self.mainTable_tableWidget.setColumnCount(len(main_table_columns_names))

        self.mainTable_tableWidget.setHorizontalHeaderLabels(main_table_columns_names)
        for row_idx, items in enumerate(main_table_columns_values):
            for column_idx, item in enumerate(items):
                _item = QtWidgets.QTableWidgetItem(item)
                self.mainTable_tableWidget.setItem(row_idx, column_idx, _item)
            
        self.mainTable_tableWidget.cellChanged.connect(self._addMainCellToArray)

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from compoundForm_formUI import Ui_Form


class CompoundForm(QtWidgets.QMainWindow, Ui_Form):
    first_choice_selected, second_choice_selected = pyqtSignal(), pyqtSignal() 
    def __init__(self, 
                main_table_columns_names, 
                main_table_column_values, 
                child_table_names, 
                child_table_columns_names, 
                child_tables_column_values):
        super(CompoundForm, self).__init__()
        self.setupUi(self)

        self.childTables_comboBox.currentTextChanged.connect(self._fillChildTableData)

        for child_table_name in child_table_columns_names:
            self.childTables_comboBox.addItem(child_table_name)

    def _fillChildTableData(self):
        ...


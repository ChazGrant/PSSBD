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


from PyQt5 import QtWidgets
from main_formUI import Ui_MainWindow


TABLES_DICT = {
    "Больные": "sick_people",
    "Заявки на вызов": "call_requests",
    "Причины вызова": "call_reason"
}

class MainWindows(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, cursor):
        super(MainWindows, self).__init__()
        self.setupUi(self)

        self.__setComboBoxes()
        self._cursor = cursor

        self.visualiseTable_pushButton.pressed.connect(self._visualizeTable)
        self.visualizeQuery_pushButton.pressed.connect(self._visualizeQuery)

    def __setComboBoxes(self):
        for table in TABLES_DICT.keys():
            self.tables_comboBox.addItem(table)

    def __setTables(self):
        ...

    def __setQueries(self):
        ...

    def _visualizeTable(self):
        self._cursor.execute("SELECT * FROM %s" % TABLES_DICT[self.tables_comboBox.currentText()])
        colnames = [desc[0] for desc in self._cursor.description]
        print(colnames)

    def _visualizeQuery(self):
        ...


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MainWindows()
    widget.show()
    app.exec_()

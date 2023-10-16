from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from UI_Forms.userEditor_formUI import Ui_MainWindow
import psycopg2

from typing import List, Any, Dict, Union


ALL_PRIVILEGES = ["SELECT", "DELETE", "UPDATE", "INSERT", "TRUNCATE", "REFERENCES", "TRIGGER"]

def showError(text: str) -> None:
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(text)
    msg.setWindowTitle("Info")
    msg.exec_()


class UserEditorForm(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, conn, cursor) -> None:
        super(UserEditorForm, self).__init__()
        self.setupUi(self)

        self._cursor = cursor
        self._conn = conn
        self._users_rights = dict()

        self.users_listWidget.currentItemChanged.connect(self._fillPrivileges)
        self.tables_listWidget.currentItemChanged.connect(self._fillPrivileges)

        self.__setUserRights()
        self._setUsers()
        self._setTables()

        self.centralWidget().setLayout(self.mainLayout)

    def _setUsers(self):
        for username in self._users_rights.keys():
            self.users_listWidget.addItem(username)

    def _setTables(self):
        tables = list()
        for tables_privileges in self._users_rights.values():
            for table in tables_privileges.keys():
                tables.append(table)
        
        for table in list(set(tables)):
            self.tables_listWidget.addItem(table)

    def __setUserRights(self):
        query = "SELECT DISTINCT grantee FROM information_schema.table_privileges \
            WHERE table_catalog = 'ambulance' AND table_schema = 'public';"
        self._cursor.execute(query)
        usernames = [user[0] for user in self._cursor.fetchall()]
        for username in usernames:
            query = "SELECT table_name, privilege_type FROM \
                information_schema.table_privileges WHERE grantee = '{}' \
                    AND table_catalog = 'ambulance' \
                        AND table_schema = 'public';".format(username)

            self._cursor.execute(query)
            self._users_rights[username] = dict()
            for data in self._cursor.fetchall():
                if data[0] not in self._users_rights[username]:
                    self._users_rights[username][data[0]] = [data[1]]
                else:
                    self._users_rights[username][data[0]].append(data[1])

    def _fillPrivileges(self):
        self.allPrivileges_listWidget.clear()
        self.grantedPrivileges_listWidget.clear()
        try:
            selected_user = self.users_listWidget.currentItem().text()
            selected_table = self.tables_listWidget.currentItem().text()
            print(selected_user)
        except AttributeError:
            return
        
        tables = self._users_rights[selected_user]
        try:
            table_privileges = tables[selected_table]
        except:
            table_privileges = []

        for table_privilege in table_privileges:
            self.grantedPrivileges_listWidget.addItem(table_privilege)
        
        for privilege in ALL_PRIVILEGES:
            if privilege not in table_privileges:
                self.allPrivileges_listWidget.addItem(privilege)


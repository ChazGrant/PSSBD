from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from UI_Forms.userEditor_formUI import Ui_MainWindow

from typing import List, Dict


ALL_PRIVILEGES = ["SELECT", "DELETE", "UPDATE", "INSERT", "TRUNCATE", "REFERENCES", "TRIGGER"]

def showError(text: str) -> None:
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(text)
    msg.setWindowTitle("Info")
    msg.exec_()


class UserEditorForm(QtWidgets.QMainWindow, Ui_MainWindow):
    window_closed = pyqtSignal()
    def __init__(self, conn, cursor) -> None:
        super(UserEditorForm, self).__init__()
        self.setupUi(self)

        self._cursor = cursor
        self._conn = conn
        self._users_rights: Dict[str, Dict[str, List[str]]] = dict()
        self._updated_users: Dict[str, List[str]] = dict()

        self.users_listWidget.currentItemChanged.connect(self._fillPrivileges)
        self.tables_listWidget.currentItemChanged.connect(self._fillPrivileges)

        self.addPrivilege_pushButton.pressed.connect(self._addPrivilege)
        self.deletePrivilege_pushButton.pressed.connect(self._deletePrivilege)
        self.updatePrivileges_pushButton.pressed.connect(self._updatePrivileges)
        self.addUser_pushButton.pressed.connect(self._addUser)
        self.deleteUser_pushButton.pressed.connect(self._deleteUser)

        self.__setUserRights()
        self._setUsers()
        self._setTables()

        self.centralWidget().setLayout(self.mainLayout)

    def closeEvent(self, a0) -> None:
        self.window_closed.emit()
        return super().closeEvent(a0)

    def _addUser(self) -> None:
        username = self.username_lineEdit.text()
        password = self.password_lineEdit.text()

        try:
            query = "CREATE ROLE {} WITH LOGIN PASSWORD '{}'".format(username, password)
            self._cursor.execute(query)

            query = "GRANT CONNECT ON DATABASE ambulance TO {}".format(username)
            self._cursor.execute(query)
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            return showError(str(e))

        self._users_rights[username] = {}
        self.users_listWidget.clear()
        self._setUsers()

    def _deleteUser(self):
        if not self.users_listWidget.currentItem():
            return
        
        selected_item = self.users_listWidget.currentItem()
        username = selected_item.text()

        if username == "amublance_admin":
            return showError("Вы не можете удалить данного пользователя")

        query = "REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM {};".format(username)
        try:
            self._cursor.execute(query)
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            return showError(str(e))
        
        query = "REVOKE ALL PRIVILEGES ON DATABASE ambulance FROM {};".format(username)
        try:
            self._cursor.execute(query)
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            return showError(str(e))

        query = "DROP ROLE {}".format(username)
        try:
            self._cursor.execute(query)
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            return showError(str(e))
        
        self._users_rights.pop(username)

        selected_row = self.users_listWidget.row(selected_item)
        self.users_listWidget.takeItem(selected_row)

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
        query = "SELECT pg_user.usename FROM pg_catalog.pg_user;"
        self._cursor.execute(query)
        all_users = [user[0] for user in self._cursor.fetchall()]
        
        for username in all_users:
            if username not in usernames:
                self._users_rights[username] = dict()
                continue

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

    def _addPrivilege(self):
        try:
            selected_user = self.users_listWidget.currentItem().text()
            selected_table = self.tables_listWidget.currentItem().text()
            selected_item = self.allPrivileges_listWidget.currentItem()
            selected_privilege = selected_item.text()
        except AttributeError:
            return
        
        try:
            self._users_rights[selected_user][selected_table].append(selected_privilege)
        except KeyError:
            self._users_rights[selected_user][selected_table] = [selected_privilege]

        if selected_user in self._updated_users.keys():
            if selected_table not in self._updated_users[selected_user]:
                self._updated_users[selected_user].append(selected_table)
        else:
            self._updated_users[selected_user] = [selected_table]

        row = self.allPrivileges_listWidget.row(selected_item)
        self.allPrivileges_listWidget.takeItem(row)

        self.grantedPrivileges_listWidget.addItem(selected_privilege)

    def _deletePrivilege(self):
        try:
            selected_user = self.users_listWidget.currentItem().text()
            selected_table = self.tables_listWidget.currentItem().text()
            selected_item = self.grantedPrivileges_listWidget.currentItem()
            selected_privilege = selected_item.text()
        except AttributeError:
            return
        
        self._users_rights[selected_user][selected_table].remove(selected_privilege)

        if selected_user in self._updated_users.keys():
            if selected_table not in self._updated_users[selected_user]:
                self._updated_users[selected_user].append(selected_table)
        else:
            self._updated_users[selected_user] = [selected_table]

        row = self.grantedPrivileges_listWidget.row(selected_item)
        self.grantedPrivileges_listWidget.takeItem(row)

        self.allPrivileges_listWidget.addItem(selected_privilege)

    def _updatePrivileges(self):
        for username in self._users_rights.keys():
            if username in self._updated_users:
                updated_tables = self._updated_users[username]
            else:
                continue
                
            for table_name, privileges in self._users_rights[username].items():
                if table_name not in updated_tables:
                    continue
                
                query = "REVOKE ALL PRIVILEGES ON {} FROM {};".format(table_name, username)
                try:
                    self._cursor.execute(query)
                    self._conn.commit()
                except Exception as e:
                    self._conn.rollback()

                if not len(privileges):
                    continue

                query = "GRANT {} ON {} TO {};".format(", ".join(privileges), table_name, username)

                try:
                    self._cursor.execute(query)
                    self._conn.commit()
                except Exception as e:
                    self._conn.rollback()
            
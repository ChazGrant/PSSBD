from PyQt5 import QtWidgets
from UI_Forms.login_formUI import Ui_MainWindow
from psycopg2 import connect, OperationalError
from main import MainWindow
from UserEditorForm import UserEditorForm
from CONFIG import CONFIG


def showMessage(text: str) -> None:
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(text)
    msg.setWindowTitle("Info")
    msg.exec_()

def showError(text: str) -> None:
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(text)
    msg.setWindowTitle("Error")
    msg.exec_()


class LoginForm(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super(LoginForm, self).__init__()
        self.setupUi(self)

        self.login_pushButton.pressed.connect(self.login)
        self.editUsers_pushButton.pressed.connect(self.openUsersEditor)

    def openUsersEditor(self) -> None:
        username = self.username_lineEdit.text()
        password = self.password_lineEdit.text()
        
        CONFIG["user"] = username
        CONFIG["password"] = password

        try:
            conn = connect(**CONFIG)
            cursor = conn.cursor()
        except OperationalError:
            return showError("Неверные данные для входа")
        
        if not username == "ambulance_admin":
            return showError("У Вас недостаточно прав")

        self.widget = UserEditorForm(conn, cursor)
        self.widget.show()
        
        self.hide()
        self.widget.window_closed.connect(self.show)

    def login(self) -> None:
        username = self.username_lineEdit.text()
        password = self.password_lineEdit.text()

        # ambulance_admin 0000
        # ambulance_operator (fN6Pn!5
        # doctor u8YVX,:2
        # nurse ]Lg4SSr4
        CONFIG["user"] = username
        CONFIG["password"] = password

        try:
            conn = connect(**CONFIG)
            cursor = conn.cursor()
        except OperationalError:
            return showError("Неверные данные для входа")

        self.widget = MainWindow(cursor, conn)
        self.widget.show()
        self.hide()

        self.username_lineEdit.setText("")
        self.password_lineEdit.setText("")

        self.widget.window_closed.connect(self.show)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = LoginForm()
    window.show()
    app.exec_()

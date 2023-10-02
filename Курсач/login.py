from PyQt5 import QtWidgets
from login_formUI import Ui_MainWindow
import psycopg2
from main import MainWindow
from CONFIG import CONFIG


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
    msg.setWindowTitle("Error")
    msg.exec_()


class LoginForm(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(LoginForm, self).__init__()
        self.setupUi(self)

        self.login_pushButton.pressed.connect(self.login)

    def login(self):
        username = self.username_textEdit.toPlainText()
        password = self.password_textEdit.toPlainText()

        if not (username or password):
            return

        # ambulance_operator (fN6Pn!5
        # doctor u8YVX,:2
        # nurse ]Lg4SSr4
        # CONFIG["user"] = "ambulance_operator"
        # CONFIG["password"] = "(fN6Pn!5"

        try:
            conn = psycopg2.connect(**CONFIG)
            cursor = conn.cursor()
        except psycopg2.OperationalError:
            return showError("Неверные данные для входа")

        self.widget = MainWindow(cursor, conn)
        self.widget.show()
        self.hide()

        self.username_textEdit.setText("")
        self.password_textEdit.setText("")

        self.widget.window_closed.connect(self.show)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = LoginForm()
    window.show()
    app.exec_()

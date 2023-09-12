from PyQt5 import QtWidgets
from login_formUI import Ui_MainWindow
import psycopg2


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
        
        CONFIG = {
            "database": "ambulance",
            "user": username,
            "password": password,
            "host": "127.0.0.1",
            "port": 5432
        }

        conn = psycopg2.connect(**CONFIG)
        cursor = conn.cursor()

        queries = ["SELECT * FROM call_reason LIMIT 10",
                    "SELECT * FROM sick_people LIMIT 10",
                    "SELECT * FROM call_requests LIMIT 10"]

        for query in queries:
            try:
                cursor.execute(query)
                print(cursor.fetchall())
            except Exception as e:
                conn.rollback()
                print(str(e))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = LoginForm()
    window.show()
    app.exec_()

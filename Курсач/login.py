from PyQt5 import QtWidgets
from loginUI import Ui_MainWindow
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
            "user": "ambulance_admin",
            "password": "secretpassword",
            "host": "192.168.1.105",
            "password": 5432
        }

        try:
            conn = psycopg2.connect(**CONFIG)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM call_reason LIMIT 10")
            print(cursor.fetchall())
            cursor.execute("SELECT * FROM sick_people LIMIT 10")
            print(cursor.fetchall())
        except Exception as e:
            raise


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = LoginForm()
    window.show()
    app.exec_()

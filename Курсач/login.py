from PyQt5 import QtWidgets
from login_formUI import Ui_MainWindow
import psycopg2
from main import MainWindow

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
        
        from CONFIG import CONFIG

        # ambulance_operator (fN6Pn!5
        # doctor u8YVX,:2
        # nurse ]Lg4SSr4
        CONFIG["user"] = "postgres"
        CONFIG["password"] = "postgres"

        print(CONFIG)
        try:
            conn = psycopg2.connect(**CONFIG)
            cursor = conn.cursor()
        except psycopg2.OperationalError:
            return

        self.widget = MainWindow(cursor, conn)
        self.widget.show()
        self.close()

        # queries = ["SELECT * FROM call_reason LIMIT 10",
        #             "SELECT * FROM sick_people LIMIT 10",
        #             "SELECT * FROM call_requests LIMIT 10"]

        # for query in queries:
        #     try:
        #         cursor.execute(query)
        #         print(cursor.fetchall())
        #     except Exception as e:
        #         conn.rollback()
        #         print(str(e))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = LoginForm()
    window.show()
    app.exec_()

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from models import create_user, get_user_by_email, check_password

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Register")

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)

        self.email_input = QLineEdit()
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def register(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        if not get_user_by_email(email):
            create_user(username, email, password)
            self.close()
        else:
            self.username_input.clear()
            self.email_input.clear()
            self.password_input.clear()
            self.email_input.setPlaceholderText("Email already exists")

def main():
    app = QApplication(sys.argv)
    register_window = RegisterWindow()
    register_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

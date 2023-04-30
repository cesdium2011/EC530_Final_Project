import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QLineEdit, QDialog, QFormLayout, QMessageBox
from PyQt5.QtCore import Qt
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, load_user
from models import User
from flask_login import login_user

class RegisterDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Register")

        layout = QFormLayout()

        self.username_input = QLineEdit()
        layout.addRow("Username", self.username_input)

        self.email_input = QLineEdit()
        layout.addRow("Email", self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addRow("Password", self.password_input)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def register(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        user = User.query.filter_by(email=email).first()
        if user:
            QMessageBox.warning(self, "Error", "Email address already exists.")
            return

        new_user = User(username=username, email=email, password=generate_password_hash(password, method="sha256"))
        db.session.add(new_user)
        db.session.commit()

        QMessageBox.information(self, "Success", "User registered successfully.")
        self.accept()

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")

        layout = QFormLayout()

        self.email_input = QLineEdit()
        layout.addRow("Email", self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addRow("Password", self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            QMessageBox.warning(self, "Error", "Please check your login details and try again.")
            return

        login_user(user)
        QMessageBox.information(self, "Success", "User logged in successfully.")
        self.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("User Management")

        layout = QVBoxLayout()

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.show_login_dialog)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.show_register_dialog)
        layout.addWidget(self.register_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_login_dialog(self):
        login_dialog = LoginDialog()
        login_dialog.exec_()

    def show_register_dialog(self):
        register_dialog = RegisterDialog()
        register_dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

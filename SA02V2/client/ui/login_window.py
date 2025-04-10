import os
import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from client.control.login_control import AuthService  # 导入 AuthService

class LoginWindow(QWidget):
    switch_to_main = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        # self.main_window=None
        self.main_window = None
        self.setWindowTitle("用户登录 / 注册")
        self.resize(300, 250)

        layout = QVBoxLayout()
        # 账号输入
        layout.addWidget(QLabel("账号："))
        self.account_input = QLineEdit()
        layout.addWidget(self.account_input)

        # 姓名输入（注册用）
        layout.addWidget(QLabel("姓名(非注册可不填)："))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        # 密码输入
        layout.addWidget(QLabel("密码："))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # 登录按钮
        self.login_btn = QPushButton("登录")
        self.login_btn.clicked.connect(self.login)
        layout.addWidget(self.login_btn)

        # 注册按钮
        self.register_btn = QPushButton("注册")
        self.register_btn.clicked.connect(self.register)
        layout.addWidget(self.register_btn)

        self.setLayout(layout)

    def login(self):
        account = self.account_input.text()
        password = self.password_input.text()
        success, result = AuthService.login(account, password)  # 调用 AuthService 的登录方法
        if success:
            QMessageBox.information(self, "成功", f"登录成功！\n当前用户ID: {result}")
            self.switch_to_main.emit(result)  # 发射信号，传递用户ID
            self.close()  # 关闭登录窗口
        else:
            QMessageBox.warning(self, "失败", result)


    def register(self):
        account = self.account_input.text()
        name = self.name_input.text()
        password = self.password_input.text()
        success, result = AuthService.register(account, name, password)  # 调用 AuthService 的注册方法
        if success:
            QMessageBox.information(self, "成功", result)
        else:
            QMessageBox.warning(self, "失败", result)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())


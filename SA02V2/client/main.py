# main.py
import sys
from PyQt5.QtWidgets import QApplication
from client.ui.login_window import LoginWindow
from client.ui.main_window import MapViewerView  # 假设 MapViewerView 已经定义好

class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)  # 创建应用程序实例
        self.login_window = LoginWindow()  # 创建登录窗口
        self.login_window.switch_to_main.connect(self.show_main_view)  # 监听登录成功后的信号
        self.login_window.show()  # 显示登录窗口

    def show_main_view(self, user_id):
        """ 显示主界面，接收 user_id 并传递给 MapViewerView """
        print(f"准备显示主界面，用户ID: {user_id}")  # 确认接收到的用户ID
        self.main_view = MapViewerView(user_id=user_id)  # 将 user_id 传递到主界面
        self.main_view.show()  # 显示主界面

    def run(self):
        """ 启动应用程序的主循环 """
        sys.exit(self.app.exec_())

# 启动应用程序
if __name__ == "__main__":
    app = MainApp()  # 创建主应用控制器
    app.run()  # 启动应用程序

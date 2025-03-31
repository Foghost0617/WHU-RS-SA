import os
import shutil

from controller.main_control import MapViewerController
from models.comment_model import CommentModel
from models.db_manager import DatabaseManager
from models.map_model import MapModel
from view.main_view import MapViewerView
import sys
from PyQt5.QtWidgets import QApplication

def get_db_path():
    """获取数据库路径，兼容调试模式和打包模式"""
    if getattr(sys, 'frozen', False):  # 运行在 PyInstaller 打包的 exe 中
        base_dir = os.path.dirname(sys.executable)  # 获取 exe 所在的目录
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))  # 开发环境

    db_path = os.path.join(base_dir, 'dbTest1.db')
    return db_path


if __name__ == "__main__":
    # 获取数据库路径
    db_path = get_db_path()

    # 创建 DatabaseManager 实例，传入数据库路径
    db_manager = DatabaseManager(db_path)

    # 输出数据库路径，用于调试
    print(f"数据库路径: {os.path.abspath(db_path)}")

    # 启动 Qt 应用
    app = QApplication(sys.argv)

    # 创建视图、模型、控制器
    view = MapViewerView()
    map_m = MapModel(db_manager)
    comment_m = CommentModel(db_manager)
    controller = MapViewerController(view, map_m, comment_m)


    # 显示视图并启动事件循环
    view.show()
    sys.exit(app.exec_())






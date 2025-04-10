import os
import platform
import sys
import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QTextEdit, QComboBox, \
    QDateEdit, QListWidget, QApplication, QMessageBox, QDialog
from PyQt5.QtCore import Qt, QDate, QDateTime
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from client.utils.config_loader import load_config

import sys
config = load_config()
ip = config.get("server_ip", "127.0.0.1")
port = config.get("server_port", 5000)
SERVER_URL = f"http://{ip}:{port}/maps"
SERVER_comment_URL = f"http://{ip}:{port}/comments"
SERVER_static_URL = f"http://{ip}:{port}"

# def get_local_ip():
#     system = platform.system()
#
#     if system == "Windows":
#         cmd = "ipconfig"
#     else:
#         cmd = "ifconfig"
#
#     output = os.popen(cmd).read()
#     lines = output.splitlines()
#
#     for line in lines:
#         if "IPv4" in line or "inet " in line:
#             if "127." not in line and "localhost" not in line:
#                 ip = line.split()[-1]
#                 if ip.count('.') == 3:
#                     return ip
#     return "127.0.0.1"
#
# ip=get_local_ip()
# SERVER_URL=f"http://{ip}:5000/maps"
# SERVER_comment_URL=f"http://{ip}:5000/comments"
# SERVER_static_URL=f"http://{ip}:5000"

print(SERVER_static_URL)


class MapViewerView(QWidget):
    def __init__(self,user_id=None):
        super().__init__()
        self.user_id = user_id  # 保存当前用户ID
        self.current_image_path = ""
        self.current_map_id = None
        self.editing_existing_map=False

        print("MapViewerView 正在初始化，用户ID为", self.user_id)

        self.init_ui()


    def init_ui(self):
        self.setWindowTitle("地图收藏家")
        self.setGeometry(700, 500, 1600, 800)

        # ========== 主布局 ==========
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        center_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # ========== 左侧区域：图像展示 ==========
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(800, 600)
        self.image_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.image_label)

        self.import_button = QPushButton("导入图像", self)
        left_layout.addWidget(self.import_button)

        self.show_button = QPushButton("查看模式", self)
        left_layout.addWidget(self.show_button)

        self.search_map_button = QPushButton("查询图像", self)
        left_layout.addWidget(self.search_map_button)

        # 地图跳转按钮（首张、上一张、下一张、末张）
        self.first_button = QPushButton("首张地图", self)
        self.prev_button = QPushButton("<<", self)
        self.next_button = QPushButton(">>", self)
        self.last_button = QPushButton("末张地图", self)

        skip_layout = QHBoxLayout()
        skip_layout.addWidget(self.first_button)
        skip_layout.addWidget(self.prev_button)
        skip_layout.addWidget(self.next_button)
        skip_layout.addWidget(self.last_button)
        left_layout.addLayout(skip_layout)

        # ========== 中间区域：地图信息 ==========
        center_layout.addWidget(QLabel("地图名称"))
        self.map_name_edit = QLineEdit(self)
        self.map_name_edit.setPlaceholderText("请输入地图名称")
        center_layout.addWidget(self.map_name_edit)

        center_layout.addWidget(QLabel("地图介质类型"))
        self.map_media_type_combo = QComboBox(self)
        self.map_media_type_combo.addItems(["纸质地图", "胶卷地图", "电子地图"])
        center_layout.addWidget(self.map_media_type_combo)

        center_layout.addWidget(QLabel("地图用途类型"))
        self.map_use_type_combo = QComboBox(self)
        self.map_use_type_combo.addItems(["地形图", "航空图", "交通图", "旅游图"])
        center_layout.addWidget(self.map_use_type_combo)

        center_layout.addWidget(QLabel("地图发行时间"))
        self.map_published_date = QDateEdit(self)
        self.map_published_date.setCalendarPopup(True)
        center_layout.addWidget(self.map_published_date)

        center_layout.addWidget(QLabel("地图收藏时间"))
        self.map_added_date = QDateEdit(self)
        self.map_added_date.setCalendarPopup(True)
        center_layout.addWidget(self.map_added_date)

        # center_layout.addWidget(QLabel("添加人"))
        # self.map_adder_edit = QLineEdit(self)
        # center_layout.addWidget(self.map_adder_edit)

        center_layout.addWidget(QLabel("地图简介"))
        self.map_description_edit = QTextEdit(self)
        self.map_description_edit.setPlaceholderText("请输入地图简介")
        center_layout.addWidget(self.map_description_edit)

        self.save_button = QPushButton("保存地图信息", self)
        self.edit_button = QPushButton("编辑地图信息", self)
        self.delete_button = QPushButton("删除地图信息", self)
        center_layout.addWidget(self.save_button)
        center_layout.addWidget(self.edit_button)
        center_layout.addWidget(self.delete_button)

        # ========== 右侧区域：评论 ==========
        right_layout.addWidget(QLabel("评论"))
        self.comment_edit = QLineEdit(self)
        self.comment_edit.setPlaceholderText("请在查看模式下输入评论内容")
        right_layout.addWidget(self.comment_edit)

        self.add_comment_button = QPushButton("添加评论", self)
        right_layout.addWidget(self.add_comment_button)

        right_layout.addWidget(QLabel("评论展示"))
        self.comment_list_widget = QListWidget(self)
        right_layout.addWidget(self.comment_list_widget)

        # ========== 合并布局 ==========
        main_layout.addLayout(left_layout)
        main_layout.addLayout(center_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

        # ========= 信号绑定 =========
        self.import_button.clicked.connect(self.import_image)
        self.show_button.clicked.connect(self.show_first_map)
        # self.search_map_button.clicked.connect(self.search_map)
        #
        self.first_button.clicked.connect(self.show_first_map)
        self.prev_button.clicked.connect(self.show_prev_map)
        self.next_button.clicked.connect(self.show_next_map)
        self.last_button.clicked.connect(self.show_last_map)
        #
        # self.save_map_signal = self.save_button.clicked
        self.save_button.clicked.connect(self.save_map_info)
        self.edit_button.clicked.connect(self.enter_editing)
        self.delete_button.clicked.connect(self.delete_map)
        #
        self.add_comment_button.clicked.connect(self.add_comment)

        self.search_map_button.clicked.connect(self.open_search_dialog)



    # def save_map_info(self):
    #     # 确保上传图像路径有效
    #     image_path = getattr(self, "uploaded_image_path", "")
    #     print(image_path)
    #     if not image_path:
    #         QMessageBox.warning(self, "警告", "请先上传地图图像！")
    #         return  # 退出保存操作
    #
    #     data = {
    #         "name": self.map_name_edit.text(),
    #         "medium_type": self.map_media_type_combo.currentText(),
    #         "usage_type": self.map_use_type_combo.currentText(),
    #         "release_time": self.map_published_date.date().toString("yyyy-MM-dd"),
    #         "added_time": self.map_added_date.date().toString("yyyy-MM-dd"),
    #         "description": self.map_description_edit.toPlainText(),
    #         "user_id": self.user_id,  # 确保user_id传递
    #         "image_path": image_path  # 保存上传后的服务器路径
    #     }
    #
    #     print(f"上传图像路径：{data['image_path']}")
    #     print(f"发送到服务器的数据：{data}")
    #
    #     try:
    #         # 发送POST请求到后端，传递数据
    #         response = requests.post(f"{SERVER_URL}/add", json=data)
    #
    #         # 检查请求是否成功
    #         response.raise_for_status()  # 检查HTTP状态码，抛出异常如果请求失败
    #
    #         # 解析返回的JSON数据
    #         result = response.json()
    #         print(f"返回结果：{result}")
    #
    #         # 根据返回的状态，显示相应的提示
    #         if result["status"] == "success":
    #             QMessageBox.information(self, "成功", "地图已保存！")
    #             self.current_map_id = result["map_id"]  # 保存新添加地图的ID
    #         else:
    #             # 如果返回失败，显示失败信息
    #             QMessageBox.warning(self, "失败", result["message"])
    #
    #     except requests.exceptions.RequestException as e:
    #         # 捕获任何请求异常，并显示网络错误
    #         QMessageBox.critical(self, "错误", f"请求失败：{e}")
    #         print(f"请求失败：{e}")
    #     except ValueError as e:
    #         # 捕获JSON解析错误
    #         QMessageBox.critical(self, "错误", f"服务器返回的数据格式错误：{e}")
    #         print(f"服务器返回的数据格式错误：{e}")

    def save_map_info(self):
        """保存地图信息，支持新增和编辑模式"""
        name = self.map_name_edit.text()
        medium_type = self.map_media_type_combo.currentText()
        usage_type = self.map_use_type_combo.currentText()
        description = self.map_description_edit.toPlainText()
        added_date = self.map_added_date.date().toString("yyyy-MM-dd")
        published_date = self.map_published_date.date().toString("yyyy-MM-dd")
        image_path=self.current_image_path

        # 构建数据体
        data = {
            "name": name,
            "medium_type": medium_type,
            "usage_type": usage_type,
            "description": description,
            "added_time": added_date,
            "release_time": published_date,
            "user_id":self.user_id,
            "image_path":image_path
        }
        print(data)
        try:
            if self.editing_existing_map:
                # 编辑信息
                data["id"] = self.current_map_id
                response = requests.put(f"{SERVER_URL}/update", json=data)
            else:
                #新增地图
                response = requests.post(f"{SERVER_URL}/add", json=data)

            response.raise_for_status()
            result = response.json()

            if result.get("status") == "success":
                QMessageBox.information(self, "成功", "地图信息已保存")
                self.is_showing_maps()  # 回到只读模式
                self.editing_existing_map=False
            else:
                QMessageBox.warning(self, "失败", result.get("message", "未知错误"))
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "错误", f"请求失败：{e}")

    def import_image(self):
        self.clear_view()
        self.is_editing_maps()
        # 打开文件对话框选择文件
        file_path, _ = QFileDialog.getOpenFileName(self, "选择地图图像", "", "Images (*.png *.jpg *.bmp *.tif)")
        if file_path:
            try:
                # 显示图像
                pixmap = QPixmap(file_path).scaled(self.image_label.width(), self.image_label.height(),
                                                   Qt.KeepAspectRatio)
                self.image_label.setPixmap(pixmap)

                # 上传图像到服务器
                with open(file_path, "rb") as f:
                    files = {"file": f}
                    response = requests.post(f"{SERVER_URL}/upload", files=files)
                    result = response.json()

                if result["status"] == "success":
                    image_url = result["path"].replace("\\", "/")  # 替换为正斜杠
                    print(f"{image_url},import")
                    self.current_image_path = image_url  # 保存服务器路径
                    QMessageBox.information(self, "成功", "图像上传成功！")
                else:
                    QMessageBox.warning(self, "失败", result["message"])

            except Exception as e:
                QMessageBox.critical(self, "错误", f"上传失败：{e}")

    def delete_map(self):
        map_id = self.current_map_id
        print(map_id)
        if not map_id:
            QMessageBox.warning(self, "警告", "没有选中地图！")
            return

        reply = QMessageBox.question(self, '确认', '确定要删除此地图吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                response = requests.delete(f"{SERVER_URL}/delete/{map_id}")
                response.raise_for_status()
                result = response.json()
                if result["status"] == "success":
                    QMessageBox.information(self, "成功", "地图已删除！")
                    self.current_map_id = None
                else:
                    QMessageBox.warning(self, "失败", result["message"])

            except requests.exceptions.RequestException as e:
                QMessageBox.critical(self, "错误", f"请求失败：{e}")
                print(f"删除失败：{e}")
        self.clear_view()


    # 实现跳转到第一张地图
    def show_first_map(self):

        self.show_map('first')
        self.is_showing_maps()

    def show_prev_map(self):

        response = requests.get(f"{SERVER_URL}/prev?current_map_id={self.current_map_id}")
        self.handle_map_response(response)
        self.is_showing_maps()

    def show_next_map(self):

        response = requests.get(f"{SERVER_URL}/next?current_map_id={self.current_map_id}")
        self.handle_map_response(response)
        self.is_showing_maps()

    def show_last_map(self):

        self.show_map('last')
        self.is_showing_maps()

    def show_map(self, direction):
        try:
            response = requests.get(f"{SERVER_URL}/{direction}")  # 获取指定方向的地图
            response.raise_for_status()
            self.handle_map_response(response)
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "错误", f"无法加载地图：{e}")
            print(f"请求失败：{e}")

    def handle_map_response(self, response):
        try:
            response.raise_for_status()  # 确保请求成功
            map_data = response.json()
            # if 'status' in map_data and map_data['status'] == 'fail':
            #     QMessageBox.warning(self, "提示", map_data['message'])
            #     return

            if 'status' in map_data and map_data['status'] == 'fail':
                if 'message' in map_data:
                    # 如果地图是第一张或最后一张，弹出提示框
                    QMessageBox.warning(self, "提示", map_data['message'])
                return

            self.clear_view()

            # 显示地图信息
            self.map_name_edit.setText(map_data['name'])
            self.map_media_type_combo.setCurrentText(map_data['medium_type'])
            self.map_use_type_combo.setCurrentText(map_data['usage_type'])
            self.map_published_date.setDate(QDate.fromString(map_data['release_time'], "yyyy-MM-dd"))
            self.map_added_date.setDate(QDate.fromString(map_data['added_time'], "yyyy-MM-dd"))
            self.map_description_edit.setPlainText(map_data['description'])
            self.current_map_id = map_data['id']
            # ✅ 再加载评论（此时才知道是哪张地图）
            self.load_comments()
            # 获取原始路径，并确保路径中的反斜杠转换为正斜杠
            image_path = map_data['image_path']
            print(f"原始路径: {image_path}")
            # 将反斜杠替换为正斜杠
            image_path = image_path.replace('\\', '/')
            print(f"转换后的路径: {image_path}")
            # 构建图像的完整 URL
            #宿舍
            image_url=f"{SERVER_static_URL}/{image_path}"
            # 打印 URL，确认路径是否正确
            print(f"图像 URL: {image_url}")

            # 下载图像数据
            image_response = requests.get(image_url)
            image_response.raise_for_status()

            # 处理图像
            image = QImage.fromData(image_response.content)

            if image.isNull():
                QMessageBox.critical(self, "错误", "无法加载图像")
                return

            # 设置图像显示到界面
            pixmap = QPixmap(image)
            pixmap = pixmap.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)

            # 更新当前地图 ID
            self.current_map_id = map_data['id']
        except requests.exceptions.RequestException as e:
            # QMessageBox.critical(self, "错误", f"无法加载地图：{e}")
            QMessageBox.critical(self, "错误", "没有更多了~")

    '''可以用的！！'''
    # def show_map(self, direction):
    #     try:
    #         response = requests.get(f"{SERVER_URL}/{direction}")  # 发送请求获取指定方向的地图
    #         response.raise_for_status()
    #         map_data = response.json()
    #         print("1")
    #
    #         if 'status' in map_data and map_data['status'] == 'fail':
    #             QMessageBox.warning(self, "提示", map_data['message'])
    #             return
    #
    #         # 显示地图信息
    #         print(map_data)
    #         self.map_name_edit.setText(map_data['name'])
    #         self.map_media_type_combo.setCurrentText(map_data['medium_type'])
    #         self.map_use_type_combo.setCurrentText(map_data['usage_type'])
    #         self.map_published_date.setDate(QDate.fromString(map_data['release_time'], "yyyy-MM-dd"))
    #         self.map_added_date.setDate(QDate.fromString(map_data['added_time'], "yyyy-MM-dd"))
    #         self.map_description_edit.setPlainText(map_data['description'])
    #
    #         # 获取原始路径，并确保路径中的反斜杠转换为正斜杠
    #         image_path = map_data['image_path']
    #         print(f"原始路径: {image_path}")
    #
    #         # 将反斜杠替换为正斜杠
    #         image_path = image_path.replace('\\', '/')
    #         print(f"转换后的路径: {image_path}")
    #
    #         # 构建图像的完整 URL
    #         image_url = f"http://10.138.177.91:5000{image_path}"
    #
    #         # 打印 URL，确认路径是否正确
    #         print(f"图像 URL: {image_url}")
    #
    #         # 下载图像数据
    #         image_response = requests.get(image_url)
    #         image_response.raise_for_status()
    #
    #         # 使用 QImage 从二进制数据创建图像
    #         image = QImage.fromData(image_response.content)
    #
    #         if image.isNull():
    #             QMessageBox.critical(self, "错误", "无法加载图像")
    #             print(f"加载图像失败，路径: {image_url}")
    #             return
    #
    #         # 转换为 QPixmap 并显示
    #         pixmap = QPixmap(image)
    #         pixmap = pixmap.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio)
    #         self.image_label.setPixmap(pixmap)
    #
    #         self.current_map_id = map_data['id']  # 保存当前地图的ID
    #     except requests.exceptions.RequestException as e:
    #         QMessageBox.critical(self, "错误", f"无法加载地图：{e}")
    #         print(f"请求失败：{e}")




    def is_showing_maps(self):
        """查看状态无法编辑，可以评论"""
        self.map_name_edit.setReadOnly(True)
        self.map_media_type_combo.setDisabled(True)
        self.map_use_type_combo.setDisabled(True)
        self.map_description_edit.setReadOnly(True)
        self.map_added_date.setDisabled(True)
        self.map_published_date.setDisabled(True)
        self.comment_edit.setReadOnly(False)
        # print("不禁用框")
        self.add_comment_button.setDisabled(False)
        # print("不禁用按键")

    def is_editing_maps(self):
        """查看状态无法编辑，可以评论"""
        self.map_name_edit.setReadOnly(False)
        self.map_media_type_combo.setDisabled(False)
        self.map_use_type_combo.setDisabled(False)
        self.map_description_edit.setReadOnly(False)
        self.map_added_date.setDisabled(False)
        self.map_published_date.setDisabled(False)
        self.comment_edit.setReadOnly(True)
        # print("不禁用框")
        self.add_comment_button.setDisabled(True)
        # print("不禁用按键")

    def enter_editing(self):
        self.is_editing_maps()
        self.editing_existing_map=True

    def clear_view(self):
        """清空视图信息"""
        self.image_label.clear()
        self.map_name_edit.clear()
        self.map_media_type_combo.setCurrentIndex(0)
        self.map_use_type_combo.setCurrentIndex(0)
        self.map_published_date.setDate(QDate.currentDate())
        self.map_added_date.setDate(QDate.currentDate())
        self.map_description_edit.clear()

        self.comment_edit.clear()  # 清空评论输入框
        self.comment_list_widget.clear()  # 清空评论列表

    def add_comment(self):
        print("!")
        content = self.comment_edit.text().strip()
        if not content:
            QMessageBox.warning(self, "提示", "评论内容不能为空")
            return

        print(self.current_map_id)

        added_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        data = {
            "content": content,
            "added_time": added_time,
            "user_id": self.user_id,
            "map_id": self.current_map_id
        }
        print(f"addcomment:{data}")
        try:
            response = requests.post(f"{SERVER_comment_URL}/add", json=data)
            response.raise_for_status()
            result = response.json()
            if result.get("status") == "success":
                QMessageBox.information(self, "成功", "评论添加成功！")
                self.comment_edit.clear()
                self.load_comments()
            else:
                QMessageBox.warning(self, "失败", result.get("message", "未知错误"))
        except Exception as e:
            QMessageBox.critical(self, "错误", f"请求失败：{e}")

    def load_comments(self):
        print(f"loadcomment{self.current_map_id}")
        if not hasattr(self, "current_map_id") or not self.current_map_id:
            print("跳过评论加载：current_map_id 未定义")
            return
        try:
            response = requests.get(f"{SERVER_comment_URL}/{self.current_map_id}")
            response.raise_for_status()
            result = response.json()
            if result.get("status") == "success":
                comments = result["comments"]
                self.comment_list_widget.clear()
                for c in comments:
                    item_text = f"[{c['added_time']}] 用户{c['user_id']}：{c['content']}"
                    self.comment_list_widget.addItem(item_text)
            else:
                QMessageBox.warning(self, "失败", result.get("message", "未知错误"))
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载评论失败：{e}")

    def open_search_dialog(self):
        dialog = SearchDialog(self)
        dialog.search_button.clicked.connect(lambda: self.perform_search(dialog))
        dialog.exec_()

    def perform_search(self, dialog):
        name = dialog.name_edit.text().strip()
        usage_type = dialog.usage_combo.currentText().strip()
        medium_type = dialog.medium_combo.currentText().strip()

        params = {
            "name": name,
            "usage_type": usage_type,
            "medium_type": medium_type
        }
        dialog.close()
        print(params)

        try:
            response = requests.get(f"{SERVER_URL}/search", params=params)
            response.raise_for_status()  # 只要没报 404 就说明查到了
            result = response.json()
            self.handle_map_response(response)
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                QMessageBox.warning(self, "未找到", "没有找到符合条件的地图")
            else:
                QMessageBox.critical(self, "错误", f"查询失败：{e}")


class SearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("查询地图")
        self.setFixedSize(500, 400)

        layout = QVBoxLayout()

        self.name_edit = QLineEdit(self)
        self.name_edit.setPlaceholderText("地图名称")
        layout.addWidget(QLabel("地图名称:"))
        layout.addWidget(self.name_edit)

        self.usage_combo = QComboBox(self)
        self.usage_combo.addItems(["地形图", "航空图", "交通图", "旅游图"])  # 自定义选项
        layout.addWidget(QLabel("使用类型:"))
        layout.addWidget(self.usage_combo)

        self.medium_combo = QComboBox(self)
        self.medium_combo.addItems(["纸质地图", "胶卷地图", "电子地图"])  # 自定义选项
        layout.addWidget(QLabel("介质类型:"))
        layout.addWidget(self.medium_combo)

        self.search_button = QPushButton("查询", self)
        layout.addWidget(self.search_button)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = MapViewerView()
    viewer.show()
    sys.exit(app.exec_())

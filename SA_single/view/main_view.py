import sys
from unittest import skipIf
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QTextEdit, QFileDialog, \
    QDateEdit, QApplication, QComboBox, QListWidget, QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MapViewerView(QWidget):
    def __init__(self):
        super().__init__()


        # 创建主布局
        self.setWindowTitle("破程序")
        self.setGeometry(700, 500, 1600, 800)

        main_layout = QHBoxLayout()#水平布局
        left_layout = QVBoxLayout()#垂直布局
        center_layout = QVBoxLayout()#垂直
        right_layout = QVBoxLayout()#垂直

        # 左侧：图像展示
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(800, 600)
        self.image_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.image_label)

        import_button = QPushButton("导入图像", self)
        left_layout.addWidget(import_button)
        show_button=QPushButton("查看模式", self)
        left_layout.addWidget(show_button)
        search_map_button=QPushButton("查询图像",self)
        left_layout.addWidget(search_map_button)


        # 添加横向布局的按钮：展示首张地图，上一张地图，下一张地图，末张地图
        skip_button = QHBoxLayout()
        # 创建四个按钮
        first_button = QPushButton("首张地图", self)
        prev_button = QPushButton("<<", self)
        next_button = QPushButton(">>", self)
        last_button = QPushButton("末张地图", self)
        # 将按钮添加到横向布局
        skip_button.addWidget(first_button)
        skip_button.addWidget(prev_button)
        skip_button.addWidget(next_button)
        skip_button.addWidget(last_button)
        # 将横向布局的按钮添加到左侧布局
        left_layout.addLayout(skip_button)

        # 中间：地图信息
        self.map_name_edit = QLineEdit(self)
        self.map_name_edit.setPlaceholderText("请输入地图名称")
        center_layout.addWidget(QLabel("地图名称"))
        center_layout.addWidget(self.map_name_edit)

        self.map_media_type_combo = QComboBox(self)
        self.map_media_type_combo.addItems(["纸质地图", "胶卷地图", "电子地图"])
        center_layout.addWidget(QLabel("地图介质类型"))
        center_layout.addWidget(self.map_media_type_combo)
        self.map_use_type_combo = QComboBox(self)
        self.map_use_type_combo.addItems(["地形图", "航空图", "交通图","旅游图"])
        center_layout.addWidget(QLabel("地图用途类型"))
        center_layout.addWidget(self.map_use_type_combo)


        self.map_published_date = QDateEdit(self)
        self.map_published_date.setCalendarPopup(True)
        center_layout.addWidget(QLabel("地图发行时间"))
        center_layout.addWidget(self.map_published_date)
        self.map_added_date = QDateEdit(self)
        self.map_added_date.setCalendarPopup(True)
        center_layout.addWidget(QLabel("地图收藏时间"))
        center_layout.addWidget(self.map_added_date)


        self.map_description_edit = QTextEdit(self)
        self.map_description_edit.setPlaceholderText("请输入地图简介")
        center_layout.addWidget(QLabel("地图简介"))
        center_layout.addWidget(self.map_description_edit)


        save_button = QPushButton("保存地图信息", self)
        edit_button = QPushButton("编辑地图信息", self)
        delete_button = QPushButton("删除地图信息", self)
        center_layout.addWidget(save_button)
        center_layout.addWidget(edit_button)
        center_layout.addWidget(delete_button)

        # 右侧：评论输入与展示
        self.comment_edit = QLineEdit(self)
        self.comment_edit.setPlaceholderText("请在查看模式下输入评论内容")
        right_layout.addWidget(QLabel("评论"))
        right_layout.addWidget(self.comment_edit)

        self.add_comment_button = QPushButton("添加评论", self)
        right_layout.addWidget(self.add_comment_button)

        # 在初始化中添加 QListWidget
        self.comment_list_widget = QListWidget(self)
        right_layout.addWidget(QLabel("评论展示"))
        right_layout.addWidget(self.comment_list_widget)

        # 布局设置
        main_layout.addLayout(left_layout)
        main_layout.addLayout(center_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

        # 信号（Signal）定义
        #信息相关
        self.import_image_signal = import_button.clicked
        self.show_map_signal=show_button.clicked
        self.save_map_signal = save_button.clicked
        self.edit_map_signal=edit_button.clicked
        self.delete_map_signal = delete_button.clicked
        self.first_map_signal = first_button.clicked
        self.prev_map_signal = prev_button.clicked
        self.next_map_signal = next_button.clicked
        self.last_map_signal = last_button.clicked
        self.search_map_signal=search_map_button.clicked

        #评论相关
        self.add_comment_signal = self.add_comment_button.clicked


class SearchMapDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("查询地图")
        self.setGeometry(820, 600, 400, 100)
        # 创建布局
        layout = QVBoxLayout()

        # 创建地图名称输入框
        self.map_name_edit = QLineEdit(self)
        self.map_name_edit.setPlaceholderText("请输入地图名称")
        layout.addWidget(QLabel("地图名称"))
        layout.addWidget(self.map_name_edit)

        # 创建地图用途下拉框
        self.use_type_combo = QComboBox(self)
        self.use_type_combo.addItems(["所有用途", "地形图", "航空图", "交通图", "旅游图"])
        layout.addWidget(QLabel("地图用途"))
        layout.addWidget(self.use_type_combo)

        # 创建地图介质类型下拉框
        self.media_type_combo = QComboBox(self)
        self.media_type_combo.addItems(["所有介质", "纸质地图", "胶卷地图", "电子地图"])
        layout.addWidget(QLabel("地图介质"))
        layout.addWidget(self.media_type_combo)

        # 创建查询按钮
        self.search_button = QPushButton("查询", self)
        layout.addWidget(self.search_button)

        # 连接查询按钮的信号
        self.search_signal=self.search_button.clicked

        # 设置对话框的布局
        self.setLayout(layout)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window =MapViewerView()
    window.show()
    sys.exit(app.exec_())
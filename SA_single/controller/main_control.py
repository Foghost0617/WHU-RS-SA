from re import search

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QDialog, QMessageBox
from PyQt5.QtCore import Qt, QDate
from view.main_view import SearchMapDialog

class MapViewerController:
    def __init__(self, view, map_model, comment_model):
        self.view = view
        self.m_model = map_model
        self.c_model = comment_model

        self.image_path = None # 存储图像路径
        self.is_showing=None #是否查看状态
        self.is_editing = False #是否编辑状态
        self.is_searching = False  #是否查询状态
        self.current_map_id = None #当前地图ID
        self.current_map_id_index=None#当前地图id索引

        # 地图元组
        self.maps = []
        # id列表
        self.map_ids = []
        #查询到的地图id列表
        self.search_map_ids=[]



        # 加载地图列表
        self.load_maps()
        self.is_none()
        print(self.current_map_id)
        print(self.current_map_id_index)

        # 初始化dialog
        self.search_dialog = SearchMapDialog()
        self.is_showing_maps()

        # 连接信号与槽
        # 地图信息相关
        self.view.import_image_signal.connect(self.import_image)  # 导入图像
        self.view.save_map_signal.connect(self.save_map_info)  # 保存信息
        self.view.show_map_signal.connect(self.enter_show_model)  # 查看(首张)图像
        self.view.delete_map_signal.connect(self.delete_map)  # 删除信息
        self.view.edit_map_signal.connect(self.enter_edit_model)  # 修改信息
        # 四个按钮：首张、上一张、下一张、末张
        self.view.first_map_signal.connect(self.show_first_map)
        self.view.prev_map_signal.connect(self.show_previous_map)
        self.view.next_map_signal.connect(self.show_next_map)
        self.view.last_map_signal.connect(self.show_last_map)

        # 评注
        self.view.add_comment_signal.connect(self.save_comment_info)

        # 查询地图
        self.view.search_map_signal.connect(self.enter_search_model)


    def is_none(self):
        if self.maps:
            self.current_map_id_index=0
            self.current_map_id=0


    def is_showing_maps(self):
        """查看状态无法编辑，可以评论"""
        self.view.map_name_edit.setReadOnly(True)
        self.view.map_media_type_combo.setDisabled(True)
        self.view.map_use_type_combo.setDisabled(True)
        self.view.map_description_edit.setReadOnly(True)
        self.view.map_added_date.setDisabled(True)
        self.view.map_published_date.setDisabled(True)
        self.view.comment_edit.setReadOnly(False)
        # print("不禁用框")
        self.view.add_comment_button.setDisabled(False)
        # print("不禁用按键")

    def is_editing_maps(self):
        """编辑状态可以修改信息，无法评论"""
        self.view.map_name_edit.setReadOnly(False)
        self.view.map_media_type_combo.setDisabled(False)
        self.view.map_use_type_combo.setDisabled(False)
        self.view.map_description_edit.setReadOnly(False)
        self.view.map_added_date.setDisabled(False)
        self.view.map_published_date.setDisabled(False)
        self.view.comment_edit.setReadOnly(True)
        # print("禁用框")
        self.view.add_comment_button.setDisabled(True)
        # print("禁用按键")


    def is_searching_maps(self):
        self.view.map_name_edit.setReadOnly(True)
        self.view.map_media_type_combo.setDisabled(True)
        self.view.map_use_type_combo.setDisabled(True)
        self.view.map_description_edit.setReadOnly(True)
        self.view.map_added_date.setDisabled(True)
        self.view.map_published_date.setDisabled(True)
        self.view.comment_edit.setReadOnly(False)
        # print("不禁用框")
        self.view.add_comment_button.setDisabled(False)
        # print("不禁用按键")


    def load_maps(self):
        """从数据库或其他数据源加载地图信息"""
        self.maps = self.m_model.get_all_maps()#返回地图元组信息
        self.map_ids=self.m_model.get_map_ids()#返回地图元组的ids

    def import_image(self):
        """纯展示，不保存"""
        self.clear_view()
        self.is_editing_maps()
        file_path, _ = QFileDialog.getOpenFileName(self.view, "选择图像", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)")
        if file_path:
            self.image_path = file_path
            # 如果用户选择了图像，加载图像
            pixmap = QPixmap(file_path)
            self.view.image_label.setPixmap(pixmap.scaled(self.view.image_label.size(), Qt.KeepAspectRatio))
            self.view.image_label.setAlignment(Qt.AlignCenter)

    def save_map_info(self):
        """保存地图信息到数据库"""
        if self.image_path:
            map_name = self.view.map_name_edit.text()
            map_description = self.view.map_description_edit.toPlainText()
            map_media_type = self.view.map_media_type_combo.currentText()
            map_use_type = self.view.map_use_type_combo.currentText()
            map_published_date = self.view.map_published_date.date().toString("yyyy-MM-dd")
            map_added_date = self.view.map_added_date.date().toString("yyyy-MM-dd")
            map_path = self.image_path
            if self.is_editing:  # 处于修改地图信息模式
                self.m_model.update_map_info(self.current_map_id, map_name, map_path, map_use_type, map_media_type,
                                             map_added_date, map_published_date, map_description)
                self.load_maps()  # 重新加载地图数据
                self.current_map_id_index = self.map_ids.index(self.current_map_id)  # 更新索引
                QMessageBox.information(self.view, "提示", "修改成功！")
            else:  # add状态
                self.m_model.add_map_info(map_name, map_path, map_use_type, map_media_type, map_added_date,
                                          map_published_date, map_description)
                self.load_maps()  # 重新加载地图数据
                self.current_map_id = self.map_ids[-1]  # 设置当前地图的ID为新插入的ID
                self.current_map_id_index = self.map_ids.index(self.current_map_id)  # 更新索引
                QMessageBox.information(self.view, "提示", "保存成功！")
        else:
            QMessageBox.information(self.view, "提示", "请先添加地图！")

        self.is_editing=False


    def show_map(self,id):
        """查看地图状态"""
        if len(self.maps)<1:
            QMessageBox.information(self.view, "提示", "请先添加地图！")
        else:
            map_data = self.m_model.get_map_data(id)  # 获取某张地图数据
            if map_data:
                self.view.image_label.setPixmap(
                    QPixmap(map_data[2]).scaled(self.view.image_label.size(), Qt.KeepAspectRatio))  # 显示地图
                self.view.image_label.setAlignment(Qt.AlignCenter)
                # 更新地图信息
                self.view.map_name_edit.setText(map_data[1])  # 设置地图名称
                self.view.map_media_type_combo.setCurrentText(map_data[4])  # 设置地图介质类型
                self.view.map_use_type_combo.setCurrentText(map_data[3])  # 设置地图用途类型
                self.view.map_published_date.setDate(QDate.fromString(map_data[6], "yyyy-MM-dd"))  # 设置地图发布日期
                self.view.map_added_date.setDate(QDate.fromString(map_data[5], "yyyy-MM-dd"))  # 设置地图收藏日期
                self.view.map_description_edit.setPlainText(map_data[7])  # 设置地图描述
                self.image_path=map_data[2]#解决保存时path参数问题
                self.current_map_id=map_data[0]#解决id问题
                print(f"show里的地图id：{self.current_map_id}")
                self.display_comments(self.current_map_id)
            else:
                QMessageBox.information(self.view, "提示", "地图不存在！")


    def show_first_map(self):
        """显示第一张地图"""
        if self.is_searching==False and len(self.map_ids)>0:
            print("展示所有列表的第一张地图")
            self.current_map_id_index = 0
            self.current_map_id=self.map_ids[0]
            # print(f"当前地图id_index：{self.current_map_id_index}")
            self.show_map(self.map_ids[0])
            # self.display_comments(self.map_ids[0])
        elif self.is_searching and len(self.search_map_ids)>0:
            print("展示查找到地图列表的第一张地图")
            self.current_map_id_index = 0
            self.current_map_id = self.search_map_ids[0]
            print(f"当前地图在查找到的地图id_index：{self.current_map_id_index}")
            self.show_map(self.search_map_ids[0])
            # self.display_comments(self.search_map_ids[0])
        else:
            QMessageBox.information(self.view, "提示", "请先添加地图！")


    def show_previous_map(self):
        """显示上一张地图"""
        if self.is_searching == False:
            print("1")
            if len(self.maps)>0 and self.current_map_id_index >0:
                print("2")
                self.current_map_id_index -= 1
                self.show_map(self.map_ids[self.current_map_id_index])
                print("3")
                # self.display_comments(self.map_ids[self.current_map_id_index])
            else:
                print("4")
                QMessageBox.information(self.view, "提示", "没有上一张啦！")

        elif self.is_searching:
            if len(self.maps)>0 and self.current_map_id_index > 0:
                self.current_map_id_index -= 1
                self.show_map(self.search_map_ids[self.current_map_id_index])
                # self.display_comments(self.search_map_ids[self.current_map_id_index])
            else:
                QMessageBox.information(self.view, "提示", "没有上一张啦！")


    def show_next_map(self):
        """显示下一张地图"""
        if self.is_searching==False :
            if len(self.maps)<1 or self.current_map_id_index==len(self.maps)-1 :
                QMessageBox.information(self.view, "提示", "没有下一张啦！")
            else :
                print(f"当前地图id_index：{self.current_map_id_index}")
                print("next2")
                self.current_map_id_index = self.current_map_id_index + 1  # 更新索引
                print(f"下一张地图id_index：{self.current_map_id_index}")
                self.show_map(self.map_ids[self.current_map_id_index])
        elif self.is_searching :
            if len(self.maps)<1 or self.current_map_id_index == len(self.search_map_ids)-1 :
                QMessageBox.information(self.view, "提示", "没有下一张啦！")
            else:
                print(f"当前查找的地图id_index：{self.current_map_id_index}")
                self.current_map_id_index = self.current_map_id_index + 1  # 更新索引
                print(f"下一张查找的地图id_index：{self.current_map_id_index}")
                self.show_map(self.search_map_ids[self.current_map_id_index])


    def show_last_map(self):
        """显示最后一张地图"""
        if self.is_searching==False:
            if len(self.maps)>0 and self.current_map_id_index>=0 :
                self.show_map(self.map_ids[-1])
                # self.display_comments(self.map_ids[self.current_map_id_index])
            else:
                QMessageBox.information(self.view, "提示", "请先添加地图！")
        elif self.is_searching:
            if len(self.maps)>0 and self.current_map_id_index>=0 :
                self.show_map(self.search_map_ids[-1])
                # self.display_comments(self.search_map_ids[self.current_map_id_index])
            else:
                QMessageBox.information(self.view, "提示", "请先添加地图！")

    def delete_map(self):
        """删除当前地图"""
        print("进入删除地图")
        if self.is_showing and len(self.map_ids)>0:
            delete_map_id = self.map_ids[self.current_map_id_index]
            delete_index = self.current_map_id_index
            print(f"删除的地图id：{delete_map_id}")
            self.m_model.delete_map_info(delete_map_id)
            print(f"成功删除地图id为{delete_map_id}的地图")
            self.c_model.delete_comments(delete_map_id)
            # 刷新地图列表
            self.load_maps()
            if len(self.map_ids) > 0:
                if delete_index >= len(self.map_ids):  # 删除的是最后一张
                    self.current_map_id_index = len(self.map_ids) - 1
                else:  # 删除的不是最后一张，则显示下一张（索引不变）
                    self.current_map_id_index = delete_index

                self.current_map_id = self.map_ids[self.current_map_id_index]
                self.show_map(self.current_map_id)
            else:
                self.clear_view()  # 如果地图列表为空，清空视图
        else:
            QMessageBox.information(self.view, "提示", "没有可删除的地图！")


    def clear_view(self):
        """清空视图信息"""
        self.view.image_label.clear()
        self.view.map_name_edit.clear()
        self.view.map_media_type_combo.setCurrentIndex(0)
        self.view.map_use_type_combo.setCurrentIndex(0)
        self.view.map_published_date.setDate(QDate.currentDate())
        self.view.map_added_date.setDate(QDate.currentDate())
        self.view.map_description_edit.clear()

        self.view.comment_edit.clear()  # 清空评论输入框
        self.view.comment_list_widget.clear()  # 清空评论列表



    def on_search(self):
        """处理查询按钮点击事件"""
        # 获取用户输入
        map_name = self.search_dialog.map_name_edit.text()
        print(map_name)
        use_type = self.search_dialog.use_type_combo.currentText()
        print(use_type)
        media_type = self.search_dialog.media_type_combo.currentText()
        print(media_type)

        self.search_map_ids = self.m_model.search_maps(map_name, use_type, media_type)#返回查询到的id列表
        print(f"查询到的地图的ids：{self.search_map_ids}")
        if self.search_map_ids:
            self.clear_view()
            print("1")
            self.show_first_map()
        else:
            QMessageBox.information(self.view, "提示", "无符合条件的地图")

    def enter_search_model(self):
        """打开查询地图对话框"""
        self.is_searching=True
        self.is_showing=False
        self.is_editing=False
        self.is_searching_maps()
        self.search_dialog.search_signal.connect(self.on_search)
        self.search_dialog.exec_()

    def enter_edit_model(self):
        self.is_editing=True
        self.is_showing=False
        self.is_searching=False
        self.is_editing_maps()

    def enter_show_model(self):
        self.is_showing=True
        self.is_editing=False
        self.is_searching=False
        self.is_showing_maps()
        self.show_first_map()

    def enter_import_model(self):
        self.is_editing=False
        self.is_showing=False
        self.is_searching=False
        self.is_editing_maps()

    def save_comment_info(self):
        self.is_showing_maps()
        comment_text = self.view.comment_edit.text()  # 获取评论内容
        print(f"评论内容：{comment_text}")
        print(f"当前地图id：{self.current_map_id}")
        if comment_text and self.current_map_id:
            print("1")
            self.c_model.add_comment(self.current_map_id, comment_text)  # 将评论保存到数据库
            print("2")
            self.display_comments(self.current_map_id)  # 更新视图显示评论
            self.view.comment_edit.clear()  # 清空输入框
        else:
            QMessageBox.information(self.view, "提示", "请先选择查看模式并确认输入了内容！")


    def display_comments(self, map_id):
        """展示评论"""
        comments = self.c_model.get_comments(map_id)  # 从模型获取该地图的评论
        self.view.comment_list_widget.clear()  # 清空现有的评论列表
        if comments:
            for comment in comments:
                #将每个评论作为一个新的列表项添加到 QListWidget 中
                self.view.comment_list_widget.addItem(f"{comment[1]}")  # 显示评论内容
        else:
            #如果没有评论，显示提示信息
            self.view.comment_list_widget.addItem("该地图暂无评论。")





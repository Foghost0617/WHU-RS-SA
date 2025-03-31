from PyQt5.QtCore import QDate

class CommentModel:
    def __init__(self, db_manager):
        self.db = db_manager

    def add_comment(self, map_id, comment_text):
        """添加评论"""
        cursor = self.db.conn.cursor()
        cursor.execute('''
            INSERT INTO comments (map_id, content, date_added)
            VALUES (?, ?, ?)
        ''', (map_id, comment_text, QDate.currentDate().toString('yyyy-MM-dd')))
        self.db.conn.commit()

    def get_comments(self, map_id):
        """获取指定地图的所有评论"""
        if not self.db.conn:
            print("数据库连接为空！")
            return []  # 返回空列表表示没有评论
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(''' 
                SELECT id, content, date_added FROM comments
                WHERE map_id = ? 
            ''', (map_id,))
            print("成功筛选评论")
            return cursor.fetchall()  # 返回所有评论
        except Exception as e:
            print(f"获取评论时出错: {e}")
            return []  # 出现错误时返回空列表

    def delete_comments(self, map_id):
        """删除指定地图的所有评论"""
        cursor = self.db.conn.cursor()
        cursor.execute('''
            DELETE FROM comments WHERE map_id = ?
        ''', (map_id,))
        print(f"正在删除 map_id={map_id} 的评论...")  # 调试用
        self.db.conn.commit()
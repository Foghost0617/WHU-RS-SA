import sqlite3
import os
import sys

"""建表"""
# class DatabaseManager:
#     def __init__(self, db_path):
#         self.db_path = db_path
#         self.conn = None
#         self.init_database()  # 初始化数据库连接
#
#
#
#     def init_database(self):
#         if self.conn is None:
#             self.conn = sqlite3.connect(self.db_path)  # 连接数据库
#             cursor = self.conn.cursor()
#
#             cursor.execute("""
#             CREATE TABLE IF NOT EXISTS maps(
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 name TEXT NOT NULL,
#                 path TEXT NOT NULL,
#                 use_type TEXT,
#                 media_type TEXT,
#                 added_date TEXT,
#                 published_date TEXT,
#                 description TEXT
#                 )
#             """
#                     )
#
#             cursor.execute('''
#             CREATE TABLE IF NOT EXISTS comments (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             map_id INTEGER NOT NULL,
#             content TEXT NOT NULL,
#             date_added TEXT,
#             FOREIGN KEY (map_id) REFERENCES maps(id)
#             )
#             '''
#                        )
#             self.conn.commit()
#
#     def close(self):
#         if self.conn:
#             self.conn.close()
#
#     def clear_database(self):
#         """清空数据库中的所有数据"""
#         if self.conn is None:
#             print("数据库未连接")
#             return
#         cursor = self.conn.cursor()
#         # 获取所有表名
#         cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#         tables = cursor.fetchall()
#
#         for table in tables:
#             table_name = table[0]
#             if table_name != "sqlite_sequence":  # 避免清空 SQLite 自增序列表
#                 cursor.execute(f"DELETE FROM {table_name};")  # 清空表数据
#                 cursor.execute(f"UPDATE sqlite_sequence SET seq = 0 WHERE name = '{table_name}';")  # 重置自增 ID
#         self.conn.commit()
#         print("数据库已清空")


"""v3"""
# class DatabaseManager:
#     def __init__(self, db_path):
#         self.db_path=db_path
#         self.conn = None
#         self.init_database()  # 初始化数据库
#
#
#
#     def init_database(self):
#         """初始化数据库"""
#         if self.conn is None:
#             self.conn = sqlite3.connect(self.db_path)  # 连接数据库
#             cursor = self.conn.cursor()
#
#             # 创建 maps 表
#             cursor.execute("""
#             CREATE TABLE IF NOT EXISTS maps(
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 name TEXT NOT NULL,
#                 path TEXT NOT NULL,
#                 use_type TEXT,
#                 media_type TEXT,
#                 added_date TEXT,
#                 published_date TEXT,
#                 description TEXT
#             )
#             """)
#
#             # 创建 comments 表
#             cursor.execute('''
#             CREATE TABLE IF NOT EXISTS comments (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 map_id INTEGER NOT NULL,
#                 content TEXT NOT NULL,
#                 date_added TEXT,
#                 FOREIGN KEY (map_id) REFERENCES maps(id)
#             )
#             ''')
#             self.conn.commit()
#
#     def close(self):
#         """关闭数据库连接"""
#         if self.conn:
#             self.conn.close()
#
#     def clear_database(self):
#         """清空数据库中的所有数据"""
#         if self.conn is None:
#             print("数据库未连接")
#             return
#         cursor = self.conn.cursor()
#         # 获取所有表名
#         cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#         tables = cursor.fetchall()
#
#         for table in tables:
#             table_name = table[0]
#             if table_name != "sqlite_sequence":  # 避免清空 SQLite 自增序列表
#                 cursor.execute(f"DELETE FROM {table_name};")  # 清空表数据
#                 cursor.execute(f"UPDATE sqlite_sequence SET seq = 0 WHERE name = '{table_name}';")  # 重置自增 ID
#         self.conn.commit()





import sqlite3
import os
import sys

class DatabaseManager:
    def __init__(self, db_path=None):
        # 获取数据库路径
        self.db_path = db_path or self.get_db_path()

        self.conn = None
        self.init_database()  # 初始化数据库连接

    def get_db_path(self):
        """获取数据库路径，兼容调试模式和打包模式"""
        if getattr(sys, 'frozen', False):  # 运行在 PyInstaller 打包的 exe 中
            base_dir = os.path.dirname(sys.executable)  # 获取 exe 所在的目录
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))  # 开发环境

        db_path = os.path.join(base_dir, 'dbTest1.db')
        return db_path

    def init_database(self):
        """初始化数据库"""
        if not os.path.exists(self.db_path):
            print(f"数据库 {self.db_path} 不存在，正在创建数据库...")
            # 如果数据库不存在，则创建它
            self.create_database()
        else:
            self.conn = sqlite3.connect(self.db_path)
            self.create_tables()

    def create_database(self):
        """创建数据库"""
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()

    def create_tables(self):
        """创建数据库表"""
        cursor = self.conn.cursor()

        # 创建 maps 表
        cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS maps(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            path TEXT NOT NULL,
            use_type TEXT,
            media_type TEXT,
            added_date TEXT,
            published_date TEXT,
            description TEXT
        )
        """)

        # 创建 comments 表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            map_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            date_added TEXT,
            FOREIGN KEY (map_id) REFERENCES maps(id)
        )
        ''')

        self.conn.commit()

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()

        def clear_database(self):
            """清空数据库中的所有数据"""
            if self.conn is None:
                print("数据库未连接")
                return
            cursor = self.conn.cursor()
            # 获取所有表名
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            for table in tables:
                table_name = table[0]
                if table_name != "sqlite_sequence":  # 避免清空 SQLite 自增序列表
                    cursor.execute(f"DELETE FROM {table_name};")  # 清空表数据
                    cursor.execute(f"UPDATE sqlite_sequence SET seq = 0 WHERE name = '{table_name}';")  # 重置自增 ID
            self.conn.commit()


# import mysql.connector
#
# # 连接到 MySQL
# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="118211yao",
#     database="map_manager"
# )
#
# # 创建一个 cursor 对象，用来执行 SQL 查询
# cursor = conn.cursor()
#
# # 执行查询语句，查看用户表
# cursor.execute("SELECT * FROM users;")
# users = cursor.fetchall()
#
# # 输出查询结果
# for user in users:
#     print(user)
#
# # 关闭连接
# cursor.close()
# conn.close()

# import mysql.connector
#
# # 连接到数据库
# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="118211yao",
#     database="map_manager"  # 一定要选对数据库
# )
# cursor = conn.cursor()
#
# # 创建 map_logs 表
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS map_logs (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT,
#     map_id INT,
#     action VARCHAR(50),
#     action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (user_id) REFERENCES users(id),
#     FOREIGN KEY (map_id) REFERENCES maps(id)
# );
# """)
#
# conn.commit()
# cursor.close()
# conn.close()
# print("map_logs 表创建成功！")



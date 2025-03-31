class MapModel:
    def __init__(self, db_manager):
        self.db = db_manager

    def add_map_info(self, name,path,use_type, media_type, added_date, published_date, description):
        """添加地图信息"""
        cursor = self.db.conn.cursor()
        cursor.execute('''
               INSERT INTO maps (name, path,use_type, media_type, added_date, published_date, description)
               VALUES (?, ?, ?, ?, ?, ?, ?)
           ''', (name, path,use_type, media_type, added_date, published_date, description))
        self.db.conn.commit()


    def get_all_maps(self):
        """从数据库中加载所有地图"""
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id, name, path,use_type, media_type, added_date, published_date, description FROM maps")  # 假设你的表中有 id, name, path 字段
        maps = cursor.fetchall()
        return maps #元组

    def get_map_ids(self):
        """获取所有地图的 ID 列表"""
        maps = self.get_all_maps()  # 获取所有地图数据
        map_ids = [map_item[0] for map_item in maps]  # 提取每个元组的第一个元素（即 id）
        return map_ids

    def get_map_data(self, map_id):
        """根据地图 ID 返回地图的数据"""
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT id, name, path, use_type, media_type, added_date, published_date, description 
            FROM maps WHERE id = ?
        """, (map_id,))  # 查询符合 map_id 的数据
        map_data = cursor.fetchone()  # 获取单条记录
        return map_data  # 返回元组（如果存在），否则返回 None

    def delete_map_info(self, map_id):
        """根据地图ID删除地图信息"""
        cursor = self.db.conn.cursor()
        cursor.execute('''DELETE FROM maps WHERE id = ?''', (map_id,))
        self.db.conn.commit()

    def update_map_info(self, map_id, name, path, use_type, media_type, added_date, published_date, description):
        """更新已有地图信息"""
        cursor = self.db.conn.cursor()
        cursor.execute('''
            UPDATE maps 
            SET name = ?, path = ?, use_type = ?, media_type = ?, added_date = ?, published_date = ?, description = ?
            WHERE id = ?
        ''', (name, path, use_type, media_type, added_date, published_date, description, map_id))
        self.db.conn.commit()


    def search_maps(self, map_name=None, use_type=None, media_type=None):
        """查询符合条件的地图，并返回 id 列表"""
        query = "SELECT id FROM maps WHERE 1=1"
        params = []

        # 动态构建查询条件
        if map_name:
            query += " AND name LIKE ?"
            params.append(f"%{map_name}%")
        if use_type and use_type != "所有用途":
            query += " AND use_type = ?"
            params.append(use_type)
        if media_type and media_type != "所有介质":
            query += " AND media_type = ?"
            params.append(media_type)

        cursor = self.db.conn.cursor()
        cursor.execute(query, params)

        # 获取查询结果并提取 id 列表
        result = cursor.fetchall()
        map_ids = [row[0] for row in result]  # 提取 id
        return map_ids  # 返回地图 ID 列表

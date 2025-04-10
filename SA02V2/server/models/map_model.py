import os

from server.database import SessionLocal
from server.models.tables import Map, MapLog,Comment

# 添加地图
def add_map(data):
    db = SessionLocal()
    print("1")
    try:
        new_map = Map(
            name=data["name"],
            medium_type=data["medium_type"],
            usage_type=data["usage_type"],
            release_time=data["release_time"],
            added_time=data["added_time"],
            description=data["description"],
            user_id=data["user_id"],
            image_path=data["image_path"]
        )
        print(f"尝试添加地图：{new_map}")
        db.add(new_map)
        db.commit()
        db.refresh(new_map)

        # 添加日志
        log = MapLog(user_id=data["user_id"], map_id=new_map.id, action="add")
        db.add(log)
        db.commit()

        return new_map.id
    except Exception as e:
        print(f"数据库操作失败：{e}")
        db.rollback()  # 回滚事务，防止数据污染
        raise  # 抛出异常，交给上层捕获
    finally:
        db.close()


def delete_map(map_id):
    db = SessionLocal()
    print("1delete?")
    try:
        # 查找地图
        map_to_delete = db.query(Map).filter(Map.id == map_id).first()

        if not map_to_delete:
            raise Exception(f"地图ID {map_id} 未找到！")

        # 打印地图信息，确保 map_to_delete 被正确获取
        print(f"查找到地图：{map_to_delete}")

        # ✅ 删除图片文件（如果存在）
        image_path = map_to_delete.image_path
        print(f"image_path: {image_path}")  # 打印出图片路径，确保它有值

        if image_path:
            # 构造绝对路径，假设项目根目录是当前工作目录
            abs_path = os.path.join(os.getcwd(), 'static', 'loads', os.path.basename(image_path))
            print(f"构造的图片路径：{abs_path}")  # 打印构造的路径，确保它正确
            if os.path.exists(abs_path):
                os.remove(abs_path)
                print(f"已删除图片文件：{abs_path}")
            else:
                print(f"图片文件不存在：{abs_path}")
        else:
            print("没有图片路径，跳过图片删除")

        # 删除相关日志
        db.query(MapLog).filter(MapLog.map_id == map_id).delete()
        db.query(Comment).filter(Comment.map_id == map_id).delete()

        # 删除地图
        db.delete(map_to_delete)
        db.commit()

        return True
    except Exception as e:
        db.rollback()
        print(f"删除地图失败：{e}")
        raise
    finally:
        db.close()



# def delete_map(map_id):
#     db = SessionLocal()
#     try:
#         # 查找地图
#         map_to_delete = db.query(Map).filter(Map.id == map_id).first()
#
#         if not map_to_delete:
#             raise Exception(f"地图ID {map_id} 未找到！")
#
#             # ✅ 删除图片文件（如果存在）
#         image_path = map_to_delete.image_path
#         print(f"delete{image_path}")
#         if image_path:
#             # 构造绝对路径，假设项目根目录是当前工作目录
#             abs_path = os.path.join(os.getcwd(), 'static', 'loads', os.path.basename(image_path))
#             if os.path.exists(abs_path):
#                 os.remove(abs_path)
#                 print(f"已删除图片文件：{abs_path}")
#             else:
#                 print(f"图片文件不存在：{abs_path}")
#
#         # 删除相关日志
#         db.query(MapLog).filter(MapLog.map_id == map_id).delete()
#         db.query(Comment).filter(Comment.map_id == map_id).delete()
#
#         # 删除地图
#         db.delete(map_to_delete)
#         db.commit()
#
#         # 删除日志记录
#         logs_to_delete = db.query(MapLog).filter(MapLog.map_id == map_id).all()
#         for log in logs_to_delete:
#             db.delete(log)
#         db.commit()
#
#         return True
#     except Exception as e:
#         db.rollback()
#         print(f"删除地图失败：{e}")
#         raise
#     finally:
#         db.close()

# 获取第一张地图
# def get_first_map():
#     db = SessionLocal()
#     try:
#         first_map = db.query(Map).order_by(Map.id.asc()).first()  # 根据id升序排序，获取第一张地图
#         if first_map:
#             return first_map
#         else:
#             raise Exception("没有地图")
#     finally:
#         db.close()
#
# # 获取上一张地图
# def get_prev_map(current_map_id):
#     db = SessionLocal()
#     try:
#         prev_map = db.query(Map).filter(Map.id < current_map_id).order_by(Map.id.desc()).first()  # 获取小于当前ID的最大地图ID
#         if prev_map:
#             return prev_map
#         else:
#             raise Exception("没有上一张地图")
#     finally:
#         db.close()
#
# # 获取下一张地图
# def get_next_map(current_map_id):
#     db = SessionLocal()
#     try:
#         next_map = db.query(Map).filter(Map.id > current_map_id).order_by(Map.id.asc()).first()  # 获取大于当前ID的最小地图ID
#         if next_map:
#             return next_map
#         else:
#             raise Exception("没有下一张地图")
#     finally:
#         db.close()
#
# # 获取最后一张地图
# def get_last_map():
#     db = SessionLocal()
#     try:
#         last_map = db.query(Map).order_by(Map.id.desc()).first()  # 根据id降序排序，获取最后一张地图
#         if last_map:
#             return last_map
#         else:
#             raise Exception("没有地图")
#     finally:
#         db.close()

def get_first_map():
    db = SessionLocal()
    try:
        first_map = db.query(Map).order_by(Map.id.asc()).first()
        if first_map:
            return first_map
        else:
            raise Exception("没有地图")
    finally:
        db.close()

def get_prev_map(current_map_id):
    db = SessionLocal()
    try:
        prev_map = db.query(Map).filter(Map.id < current_map_id).order_by(Map.id.desc()).first()
        if prev_map:
            return prev_map
        else:
            raise Exception("没有上一张地图")
    finally:
        db.close()

def get_next_map(current_map_id):
    db = SessionLocal()
    try:
        next_map = db.query(Map).filter(Map.id > current_map_id).order_by(Map.id.asc()).first()
        if next_map:
            return next_map
        else:
            raise Exception("没有下一张地图")
    finally:
        db.close()

def get_last_map():
    db = SessionLocal()
    try:
        last_map = db.query(Map).order_by(Map.id.desc()).first()
        if last_map:
            return last_map
        else:
            raise Exception("没有地图")
    finally:
        db.close()



def update_map_by_id(map_id, updated_data):
    db = SessionLocal()
    try:
        map_to_update = db.query(Map).filter(Map.id == map_id).first()
        if not map_to_update:
            raise Exception(f"地图ID {map_id} 未找到！")

        map_to_update.name = updated_data['name']
        map_to_update.medium_type = updated_data['medium_type']
        map_to_update.usage_type = updated_data['usage_type']
        map_to_update.description = updated_data['description']
        map_to_update.added_time = updated_data['added_time']
        map_to_update.release_time = updated_data['release_time']
        map_to_update.image_path=updated_data['image_path']

        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"更新地图失败：{e}")
        raise
    finally:
        db.close()

#
# # 辅助函数：Map对象转字典
# def map_to_dict(m):
#     if not m:
#         return None
#     return {
#         "id": m.id,
#         "name": m.name,
#         "medium_type": m.medium_type,
#         "usage_type": m.usage_type,
#         "release_time": str(m.release_time),
#         "added_time": str(m.added_time),
#         "description": m.description,
#         "user_id": m.user_id,
#         "image_path": m.image_path
#     }

def search_first_map(name, usage_type, medium_type):
    db = SessionLocal()
    try:
        query = db.query(Map)

        if name:
            query = query.filter(Map.name.ilike(f"%{name}%"))
        if usage_type:
            query = query.filter(Map.usage_type == usage_type)
        if medium_type:
            query = query.filter(Map.medium_type == medium_type)

        first_map = query.first()
        if not first_map:
            return None

        return {
            "id": first_map.id,
            "name": first_map.name,
            "medium_type": first_map.medium_type,
            "usage_type": first_map.usage_type,
            "release_time": first_map.release_time.strftime("%Y-%m-%d"),
            "added_time": first_map.added_time.strftime("%Y-%m-%d"),
            "description": first_map.description,
            "image_path": first_map.image_path
        }
    finally:
        db.close()

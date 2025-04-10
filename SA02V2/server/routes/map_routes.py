# backend/routes/maps_routes.py
import os

from flask import Blueprint, request, jsonify
from server.models import map_model
from werkzeug.utils import secure_filename
from server.database import SessionLocal  # 导入获取数据库会话的函数

maps_bp = Blueprint("maps", __name__, url_prefix="/maps")

@maps_bp.route("/add", methods=["POST"])
def add_map():
    data = request.json
    print(f"接收到的数据: {data}")  # 打印请求数据

    required_fields = ["name", "medium_type", "usage_type", "release_time", "added_time","description", "user_id", "image_path"]
    if not all(field in data for field in required_fields):
        return jsonify({"status": "fail", "message": "信息不完整"}), 400

    try:
        map_id = map_model.add_map(data)
        return jsonify({"status": "success", "message": "添加成功", "map_id": map_id})
    except Exception as e:
        print(f"服务器端错误：{e}")  # 输出异常信息
        return jsonify({"status": "error", "message": "服务器内部错误"}), 500


# 设置允许的文件类型和上传目录
ALLOWED_EXTENSIONS = {'png', 'jpg', 'bmp', 'tif'}
UPLOAD_FOLDER = 'static/uploads'  # 上传路径

# 检查文件扩展名是否被允许
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@maps_bp.route("/upload", methods=["POST"])
def upload_map_image():
    if "file" not in request.files:
        return jsonify({"status": "fail", "message": "没有上传文件"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"status": "fail", "message": "没有选择文件"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)  # 保存路径

        try:
            # 确保保存目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file.save(file_path)

            # 返回图像的相对路径（前端可以使用）
            return jsonify({"status": "success", "path": f"/{file_path}"}), 200
        except Exception as e:
            print(f"文件上传失败：{e}")
            return jsonify({"status": "fail", "message": "文件上传失败"}), 500
    else:
        return jsonify({"status": "fail", "message": "文件类型不支持"}), 400



@maps_bp.route("/delete/<int:map_id>", methods=["DELETE"])
def delete_map(map_id):
    print(f"尝试删除地图ID：{map_id}")

    try:
        print("routes?")
        success = map_model.delete_map(map_id)
        if success:
            return jsonify({"status": "success", "message": "地图已删除"})
        else:
            return jsonify({"status": "fail", "message": "删除失败"}), 400
    except Exception as e:
        print(f"删除地图出错：{e}")
        return jsonify({"status": "error", "message": "服务器内部错误"}), 500


# @maps_bp.route("/first", methods=["GET"])
# def first_map():
#     try:
#         first_map = map_model.get_first_map()
#         return jsonify({
#             "status": "success",
#             "id": first_map.id,
#             "name": first_map.name,
#             "medium_type": first_map.medium_type,
#             "usage_type": first_map.usage_type,
#             "release_time": first_map.release_time,
#             "added_time": first_map.added_time,
#             "description": first_map.description,
#             "image_path": first_map.image_path
#         })
#     except Exception as e:
#         return jsonify({"status": "fail", "message": str(e)}), 500
#
#
# @maps_bp.route("/prev", methods=["GET"])
# def prev_map():
#     current_map_id = request.args.get('current_map_id', type=int)
#
#     if current_map_id is None:
#         return jsonify({"status": "fail", "message": "current_map_id 参数缺失"}), 400
#
#     try:
#         prev_map = map_model.get_prev_map(current_map_id)
#         if not prev_map:
#             return jsonify({"status": "fail", "message": "没有上一张地图"}), 404
#         return jsonify({
#             "status": "success",
#             "id": prev_map.id,
#             "name": prev_map.name,
#             "medium_type": prev_map.medium_type,
#             "usage_type": prev_map.usage_type,
#             "release_time": prev_map.release_time,
#             "added_time": prev_map.added_time,
#             "description": prev_map.description,
#             "image_path": prev_map.image_path
#         })
#     except Exception as e:
#         return jsonify({"status": "fail", "message": str(e)}), 500
#
#
# @maps_bp.route("/next", methods=["GET"])
# def next_map():
#     current_map_id = request.args.get('current_map_id', type=int)
#
#     if current_map_id is None:
#         return jsonify({"status": "fail", "message": "current_map_id 参数缺失"}), 400
#
#     try:
#         next_map = map_model.get_next_map(current_map_id)
#         if not next_map:
#             return jsonify({"status": "fail", "message": "没有下一张地图"}), 404
#         return jsonify({
#             "status": "success",
#             "id": next_map.id,
#             "name": next_map.name,
#             "medium_type": next_map.medium_type,
#             "usage_type": next_map.usage_type,
#             "release_time": next_map.release_time,
#             "added_time": next_map.added_time,
#             "description": next_map.description,
#             "image_path": next_map.image_path
#         })
#     except Exception as e:
#         return jsonify({"status": "fail", "message": str(e)}), 500
# @maps_bp.route("/last", methods=["GET"])
# def last_map():
#     try:
#         last_map = map_model.get_last_map()
#         return jsonify({
#             "status": "success",
#             "id": last_map.id,
#             "name": last_map.name,
#             "medium_type": last_map.medium_type,
#             "usage_type": last_map.usage_type,
#             "release_time": last_map.release_time,
#             "added_time": last_map.added_time,
#             "description": last_map.description,
#             "image_path": last_map.image_path
#         })
#     except Exception as e:
#         return jsonify({"status": "fail", "message": str(e)}), 500



#
# # 删除地图
# @maps_bp.route("/<int:map_id>", methods=["DELETE"])
# def delete_map(map_id):
#     user_id = request.args.get("user_id", type=int)
#     if not user_id:
#         return jsonify({"status": "fail", "message": "缺少 user_id"}), 400
#
#     map_model.delete_map(map_id, user_id)
#     return jsonify({"status": "success", "message": "删除成功"})
#
# # 模糊查找地图
# @maps_bp.route("/search", methods=["GET"])
# def search_maps():
#     keyword = request.args.get("keyword", "")
#     results = map_model.search_maps(keyword)
#     return jsonify({"status": "success", "maps": results})
#
# # 获取单张地图信息
# @maps_bp.route("/<int:map_id>", methods=["GET"])
# def get_map(map_id):
#     result = map_model.get_map_by_id(map_id)
#     if result:
#         return jsonify({"status": "success", "map": result})
#     return jsonify({"status": "fail", "message": "地图不存在"}), 404
#
# # 修改地图信息
# @maps_bp.route("/<int:map_id>", methods=["PUT"])
# def update_map(map_id):
#     data = request.json
#     user_id = data.get("user_id")
#     if not user_id:
#         return jsonify({"status": "fail", "message": "缺少 user_id"}), 400
#
#     updated = map_model.update_map(map_id, data)
#     return jsonify({"status": "success", "message": "修改成功"})
#
# # 浏览地图（前后跳转）
# @maps_bp.route("/nav", methods=["GET"])
# def navigate_maps():
#     current_id = request.args.get("current_id", type=int)
#     direction = request.args.get("direction")
#     result = map_model.navigate_map(current_id, direction)
#     if result:
#         return jsonify({"status": "success", "map": result})
#     return jsonify({"status": "fail", "message": "无法跳转"}), 404
#
#
# @maps_bp.route("/upload", methods=["POST"])
# def upload_map_image():
#     if "file" not in request.files:
#         return jsonify({"status": "error", "message": "没有文件"})
#
#     file = request.files["file"]
#     if file.filename == "":
#         return jsonify({"status": "error", "message": "文件名为空"})
#
#     filename = secure_filename(file.filename)
#
#     # 保存路径（确保 static/uploads 目录存在）
#     upload_folder = os.path.join(os.getcwd(), "static", "uploads")
#     os.makedirs(upload_folder, exist_ok=True)
#     save_path = os.path.join(upload_folder, filename)
#     file.save(save_path)
#
#     # 返回可用于访问的 URL 路径
#     return jsonify({
#         "status": "success",
#         "path": f"/static/uploads/{filename}"
#     })


# 获取第一张地图
@maps_bp.route("/first", methods=["GET"])
def first_map():
    try:
        first_map = map_model.get_first_map()
        return jsonify({
            "status": "success",
            "id": first_map.id,
            "name": first_map.name,
            "medium_type": first_map.medium_type,
            "usage_type": first_map.usage_type,
            "release_time": first_map.release_time,
            "added_time": first_map.added_time,
            "description": first_map.description,
            "image_path": first_map.image_path
        })
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)}), 500

# 获取上一张地图
@maps_bp.route("/prev", methods=["GET"])
def prev_map():
    current_map_id = request.args.get('current_map_id', type=int)
    try:
        prev_map = map_model.get_prev_map(current_map_id)
        return jsonify({
            "status": "success",
            "id": prev_map.id,
            "name": prev_map.name,
            "medium_type": prev_map.medium_type,
            "usage_type": prev_map.usage_type,
            "release_time": prev_map.release_time,
            "added_time": prev_map.added_time,
            "description": prev_map.description,
            "image_path": prev_map.image_path
        })
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)}), 500

# 获取下一张地图
@maps_bp.route("/next", methods=["GET"])
def next_map():
    current_map_id = request.args.get('current_map_id', type=int)
    try:
        next_map = map_model.get_next_map(current_map_id)
        return jsonify({
            "status": "success",
            "id": next_map.id,
            "name": next_map.name,
            "medium_type": next_map.medium_type,
            "usage_type": next_map.usage_type,
            "release_time": next_map.release_time,
            "added_time": next_map.added_time,
            "description": next_map.description,
            "image_path": next_map.image_path
        })
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)}), 500

# 获取最后一张地图
@maps_bp.route("/last", methods=["GET"])
def last_map():
    try:
        last_map = map_model.get_last_map()
        return jsonify({
            "status": "success",
            "id": last_map.id,
            "name": last_map.name,
            "medium_type": last_map.medium_type,
            "usage_type": last_map.usage_type,
            "release_time": last_map.release_time,
            "added_time": last_map.added_time,
            "description": last_map.description,
            "image_path": last_map.image_path
        })
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)}), 500

@maps_bp.route('/update', methods=['PUT'])
def update_map():
    data = request.get_json()
    map_id = data.get('id')

    if not map_id:
        return jsonify({'status': 'fail', 'message': '缺少地图ID'}), 400

    try:
        map_model.update_map_by_id(map_id, data)
        return jsonify({'status': 'success', 'message': '地图信息更新成功'})
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'更新失败：{e}'}), 500

@maps_bp.route("/search", methods=["GET"])
def search_map():
    name = request.args.get("name", "")
    usage_type = request.args.get("usage_type", "")
    medium_type = request.args.get("medium_type", "")

    try:
        map_data = map_model.search_first_map(name, usage_type, medium_type)
        if map_data:
            return jsonify(map_data)
        else:
            return jsonify({"status": "fail", "message": "未找到符合条件的地图"}), 404
    except Exception as e:
        print(f"地图查询出错: {e}")
        return jsonify({"status": "error", "message": "服务器内部错误"}), 500

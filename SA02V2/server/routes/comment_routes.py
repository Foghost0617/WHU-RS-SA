import os

from flask import Blueprint, request, jsonify
from server.models import comment_model
from werkzeug.utils import secure_filename

comments_bp = Blueprint("comments", __name__, url_prefix="/comments")

@comments_bp.route("/add", methods=["POST"])
def add_comment():
    data = request.json
    required_fields = ["content", "added_time", "user_id", "map_id"]
    if not all(field in data for field in required_fields):
        return jsonify({"status": "fail", "message": "信息不完整"}), 400

    try:
        comment_id = comment_model.add_comment(data)
        return jsonify({"status": "success", "comment_id": comment_id})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@comments_bp.route("/<int:map_id>", methods=["GET"])
def get_comments(map_id):
    try:
        comments = comment_model.get_comments_by_map(map_id)
        result = [{
            "id": c.id,
            "content": c.content,
            "added_time": c.added_time.strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": c.user_id
        } for c in comments]

        return jsonify({"status": "success", "comments": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# backend/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from server.models.tables import User
from server.database import SessionLocal

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    account = data.get("account")
    name = data.get("name")
    password = data.get("password")

    db = SessionLocal()
    if db.query(User).filter_by(account=account).first():
        db.close()
        return jsonify({"status": "fail", "message": "账号已存在"}), 400

    new_user = User(account=account, name=name, password=password)
    db.add(new_user)
    db.commit()
    db.close()
    return jsonify({"status": "success", "message": "注册成功"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    account = data.get("account")
    password = data.get("password")

    db = SessionLocal()
    user = db.query(User).filter_by(account=account, password=password).first()
    db.close()

    if user:
        return jsonify({"status": "success", "message": "登录成功", "user_id": user.id})
    else:
        return jsonify({"status": "fail", "message": "账号或密码错误"}), 401

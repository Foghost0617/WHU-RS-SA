# services/auth_service.py
import os
import platform

import requests
from client.utils.config_loader import load_config
import sys

config = load_config()
ip = config.get("server_ip", "127.0.0.1")
port = config.get("server_port", 5000)

SERVER_URL = f"http://{ip}:5000/auth"

class AuthService:
    @staticmethod
    def login(account, password):
        if not account or not password:
            return False, "请填写账号和密码"
        try:
            res = requests.post(f"{SERVER_URL}/login", json={
                "account": account,
                "password": password
            })
            if res.status_code == 200:
                return True, res.json().get("user_id")
            else:
                return False, res.json().get("message")
        except Exception as e:
            return False, f"请求失败：{str(e)}"

    @staticmethod
    def register(account, name, password):
        if not account or not name or not password:
            return False, "请填写所有注册信息"

        try:
            res = requests.post(f"{SERVER_URL}/register", json={
                "account": account,
                "name": name,
                "password": password
            })
            if res.status_code == 201:
                return True, "注册成功！请登录"
            else:
                return False, res.json().get("message")
        except Exception as e:
            return False, f"请求失败：{str(e)}"


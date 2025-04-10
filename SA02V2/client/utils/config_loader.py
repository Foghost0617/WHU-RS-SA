import os
import sys
import json

# def load_config():
#     if hasattr(sys, '_MEIPASS'):
#         # 打包后执行 exe，从临时目录中找
#         base_path = sys._MEIPASS
#     else:
#         # 调试阶段，从项目根目录找（main.py 直接 run 时）
#         base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
#
#     config_path = os.path.join(base_path, "config.json")
#
#     print(f"[DEBUG] 当前 config 路径: {config_path}")  # 可选调试输出
#
#     if not os.path.exists(config_path):
#         raise FileNotFoundError(f"配置文件不存在: {config_path}")
#
#     with open(config_path, "r", encoding="utf-8") as f:
#         return json.load(f)
import os
import sys
import json
import shutil

import os
import sys
import json

def load_config():
    # 判断是否在打包后的环境中运行
    if hasattr(sys, '_MEIPASS'):
        # 在打包后的环境中，配置文件应在临时目录
        base_path = os.path.dirname(sys.argv[0])
    else:
        # 在开发模式下，配置文件在根目录
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    config_path = os.path.join(base_path, "config.json")

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

# 调用 load_config 读取配置文件
config = load_config()
print(config)

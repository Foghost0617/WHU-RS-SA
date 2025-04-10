from socket import socket

from flask import Flask
from routes.auth_routes import auth_bp
from routes.map_routes import maps_bp
from routes.comment_routes import comments_bp
from database import Base, engine

app = Flask(__name__, static_url_path='/static', static_folder='static')  #设置静态路径

Base.metadata.create_all(bind=engine)

# 注册蓝图
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(maps_bp, url_prefix="/maps")
app.register_blueprint(comments_bp, url_prefix="/comments")
print(app.url_map)



@app.route("/")
def index():
    return "Flask 运行成功！🎉"

if __name__ == "__main__":


    app.run(host="0.0.0.0", port=5000,debug=True)


from flask import Flask, jsonify
from flask_cors import CORS
from connect import create_app  # 导入封装的 create_app()
from config import Config
from app.routes.ums.User import user_bp

app = create_app()
if not app:
    print("❌ Flask 应用初始化失败，检查数据库连接")
    exit(1)
CORS(app)  # 允许 Vue 访问

# 注册蓝图
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

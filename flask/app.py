from flask import Flask, jsonify
from flask_cors import CORS
from connect import create_app  # 导入封装的 create_app()
from flasgger import Swagger
from config import Config

app = create_app()
if not app:
    print("❌ Flask 应用初始化失败，检查数据库连接")
    exit(1)
CORS(app)  # 允许 Vue 访问

# 加载 Flasgger 配置
swagger = Swagger(app, template=Config.SWAGGER_CONFIG)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

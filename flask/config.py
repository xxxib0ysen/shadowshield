import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

class Config:
    # 数据库
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DB")

    # Flasgger
    SWAGGER_CONFIG = {
        "swagger": "2.0",
        "info": {
            "title": "ShadowShield API 文档",
            "description": "这是 ShadowShield 的 API 文档",
            "version": "1.0.0",
        },
        "host": "127.0.0.1:5000",
        "basePath": "/api",
        "schemes": ["http"],
    }

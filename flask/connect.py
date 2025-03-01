import pymysql
from flask import Flask
from config import Config

def create_connection():
    try:
        conn = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("✅ 数据库连接成功")
        return conn
    except pymysql.MySQLError as e:
        print(f"❌ 数据库连接失败: {str(e)}")
        raise


def create_app():
    """初始化 Flask 应用"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # 挂载 MySQL 连接到 Flask app
    app.mysql = create_connection()

    return app
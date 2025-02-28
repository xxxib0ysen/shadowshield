from flask import Flask
from app.extensions import db
from config import Config
from app.models import init_models  # 导入模型初始化函数
from sqlalchemy import text


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)

    # 在应用上下文中执行初始化
    with app.app_context():
        try:
            # 初始化数据库模型
            app.models = init_models()  # 挂载模型到app实例

            # 验证数据库连接
            db.session.execute(text("SELECT 1")).scalar()
            app.logger.info("数据库连接成功")
        except Exception as e:
            app.logger.critical(f"数据库连接失败: {str(e)}")
            raise  # 直接抛出异常，防止应用以错误状态运行



    return app
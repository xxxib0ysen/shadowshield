from flask import Flask, jsonify
from flask_cors import CORS

from app.routes.proxy.proxy import proxy_bp
from app.routes.rule.adblock_source import adblock_bp
from app.routes.control.custom_rule import custom_bp
from app.routes.rule.website_control import website_bp
from app.routes.system.setting import setting_bp
from app.routes.ums.Login import login_bp
from app.routes.ums.Menu import menu_bp
from app.routes.ums.Permission import permission_bp
from app.routes.ums.Resource import resource_bp
from app.routes.ums.ResourceCategory import resource_category_bp
from app.routes.ums.Role import role_bp
from connect import create_app  # 导入封装的 create_app()
from config import Config
from app.routes.ums.User import user_bp
from app.utils.task_scheduler import start_scheduler

app = create_app()
if not app:
    print("❌ Flask 应用初始化失败，检查数据库连接")
    exit(1)
CORS(app)  # 允许 Vue 访问

# 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(role_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(permission_bp)
app.register_blueprint(resource_bp)
app.register_blueprint(resource_category_bp)
app.register_blueprint(login_bp)

app.register_blueprint(adblock_bp)
with app.app_context():
    start_scheduler()
app.register_blueprint(website_bp)
app.register_blueprint(custom_bp)
app.register_blueprint(setting_bp)
app.register_blueprint(proxy_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

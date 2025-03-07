from flask import Blueprint, request
from app.services.ums.LoginService import login_user, refresh_token, get_current_user, logout
from app.utils.response import error_response

login_bp = Blueprint("login", __name__, url_prefix="/userLogin")

# 用户登录
@login_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    return login_user(data.get("username"), data.get("password"))

# 刷新 Token
@login_bp.route("/refresh", methods=["GET"])
def refresh_token_api():
    token = request.headers.get("Authorization")
    if not token:
        return error_response("未提供 Token", 401)
    return refresh_token(token)

# 获取当前用户信息
@login_bp.route("/info", methods=["GET"])
def user_info_api():
    token = request.headers.get("Authorization")
    if not token:
        return error_response("未提供 Token", 401)
    return get_current_user(token)

# 退出登录
@login_bp.route("/logout", methods=["POST"])
def logout_api():
    return logout()

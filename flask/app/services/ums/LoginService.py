import jwt
import datetime
from flask import request
from app.utils.response import success_response, error_response
from connect import create_connection
from app.utils.common import hash_pwd
from config import secret_key, token_expiration,token_fresh_expiration

def generate_token(user_id, username,exp_seconds=token_expiration):
    # 生成 JWT Token
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=token_expiration)
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")

#   解码 JWT Token
def decode_token(token):
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# 登录
def login_user(username, password):
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("select user_id, username, password from ums_user where username=%s", (username,))
            user = cursor.fetchone()
            if not user or user["password"] != hash_pwd(password):
                return error_response("用户名或密码错误", 401)

            token = generate_token(user["user_id"], user["username"])
            return success_response({"token": token}, "登录成功")
    finally:
        conn.close()

#     刷新 Token
def refresh_token(old_token):
    decoded = decode_token(old_token)
    if not decoded:
        return error_response("Token 已过期或无效", 401)

    new_token = generate_token(decoded["user_id"], decoded["username"], token_fresh_expiration)
    return success_response({"token": new_token}, "Token 刷新成功")

#   获取当前登录用户信息
def get_current_user(token):
    decoded = decode_token(token)
    if not decoded:
        return error_response("Token 无效或已过期", 401)

    return success_response({"user_id": decoded["user_id"], "username": decoded["username"]}, "获取用户信息成功")

#  登出  前端删除token
def logout():
    return success_response("登出成功")
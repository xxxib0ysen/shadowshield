import re
from datetime import datetime
import hashlib

import pymysql
from flask import request

from app.utils.response import error_response
from connect import create_connection

# 获取请求中的 JSON 数据
def get_json():
    try:
        return request.get_json()
    except Exception:
        return None

# 验证请求参数是否完整
def validate_params(required_params, data):
    missing_params = [param for param in required_params if param not in data]
    return missing_params

# 密码哈希加密
def hash_pwd(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 检查用户是否存在
def user_exist(user_id):
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("select user_id from ums_user where user_id=%s", (user_id,))
            return cursor.fetchone() is not None
    finally:
        conn.close()

# 检查角色是否存在
def role_exist(role_id):
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("select role_id from ums_role where role_id=%s", (role_id,))
            return cursor.fetchone() is not None
    finally:
        conn.close()

#   检查菜单是否存在
def menu_exist(menu_id):
    if menu_id is None:
        return False
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("select menu_id from ums_menu where menu_id=%s", (menu_id,))
            return cursor.fetchone() is not None
    finally:
        conn.close()

# 检查资源分类是否存在
def resource_category_exist(category_id):
    if category_id is None:
        return False
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("select category_id from ums_resource_category where category_id=%s", (category_id,))
            return cursor.fetchone() is not None
    finally:
        conn.close()

# 检查资源是否存在
def resource_exist(resource_id):
    if resource_id is None:
        return False
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("select resource_id from ums_resource where resource_id=%s", (resource_id,))
            return cursor.fetchone() is not None
    finally:
        conn.close()

# 检查权限是否存在
def permission_exist(permission_id):
    if permission_id is None:
        return False
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("select permission_id from ums_permission where permission_id=%s", (permission_id,))
            return cursor.fetchone() is not None
    finally:
        conn.close()

# 分页
def paginate_query(page, page_size):
    page = max(1, page)  # 确保页码至少为 1
    page_size = min(100, max(1, page_size))  # 限制每页数量最大 100，最小 1
    offset = (page - 1) * page_size
    return offset, page_size

# 格式化时间
def format_datetime(dt):
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(dt, str):
        try:
            return datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return dt
    return None

# 验证 URL 是否符合格式，支持通配符 '*' 和 '>'
def validate_url(url):
    pattern = re.compile(
        r'^(https?:\/\/)?([a-zA-Z0-9*>\-._~:/?#@!$&\'()*+,;=%]+)$'
    )
    return bool(pattern.match(url))
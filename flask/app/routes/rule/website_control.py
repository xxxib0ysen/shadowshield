import pymysql
from flask import Blueprint, request
from app.services.rule.WebsiteService import (
    get_website_type, add_type, delete_website_type,
    add_website_rule, delete_website_rule, update_website_status, get_website_rule
)
from app.utils.response import success_response, error_response

website_bp = Blueprint("website_control", __name__,url_prefix="/website_control")

# 获取所有网站类型
@website_bp.route("/type", methods=["GET"])
def list_type():
    return get_website_type()

# 添加网站类型
@website_bp.route("/type/add", methods=["POST"])
def add_website_type():
    data = request.get_json()
    type_name = data.get("type_name")
    return add_type(type_name)

# 删除网站类型
@website_bp.route("/type/delete", methods=["POST"])
def delete_type():
    data = request.get_json()
    type_id = data.get("type_id")
    if not type_id:
        return error_response("type_id不能为空")
    return delete_website_type(type_id)

# 添加网站访问规则（支持单个/多个网址）
@website_bp.route("/add", methods=["POST"])
def add_rule():
    data = request.get_json()
    return add_website_rule(data)

# 删除网站规则
@website_bp.route("/delete", methods=["POST"])
def delete_rule():
    data = request.get_json()
    website_id = data.get("website_id")
    if not website_id:
        return error_response("website_id不能为空")
    return delete_website_rule(website_id)

# 启用/禁用网站规则
@website_bp.route("/updateStatus", methods=["POST"])
def update_status():
    data = request.get_json()
    website_id = data.get("website_id")
    status = data.get("status")
    if not website_id or status not in [0, 1]:
        return error_response("参数错误，website_id 必须存在，状态值必须为 0（禁用）或 1（启用）")
    return update_website_status(website_id, status)


# 获取所有网站规则
@website_bp.route("/list", methods=["GET"])
def list_rule():
    return get_website_rule()

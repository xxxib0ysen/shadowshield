from flask import Blueprint,request
from app.services.ums.UserService import *
from app.utils.response import *
from app.utils.common import *

user_bp = Blueprint('user', __name__, url_prefix="/api/users")

@user_bp.route("/",methods=["GET"])
def list_users():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    search = request.args.get("search", "",type=str)
    return get_users(page, per_page, search)

@user_bp.route("/", methods=["POST"])
def add_user():
    data = get_json()
    required_fields = ["username", "fullname", "password", "status"]
    missing = validate_params(required_fields, data)
    if missing:
        return error_response(f"缺少参数: {', '.join(missing)}", 400)
    if data["status"] not in [0,1]:
        return error_response("status 只能是 0（禁用）或 1（启用）", 400)
    return create_user(data)

@user_bp.route("/<int:user_id>", methods=["PUT"])
def edit_user(user_id):
    data = get_json()
    if not data:
        return error_response("请求体不能为空", 400)
    return update_user(user_id, data)

@user_bp.route("/<int:user_id>", methods=["DELETE"])
def remove_user(user_id):
    return delete_user(user_id)

@user_bp.route("/<int:user_id>/status", methods=["PUT"])
def change_user_status(user_id):
    # 启用/禁用用户
    data = get_json()
    status = data.get("status")
    if status not in [0, 1]:
        return error_response("状态值必须为 0 或 1", 400)
    return toggle_user_status(user_id, status)

@user_bp.route("/<int:user_id>/roles", methods=["PUT"])
def assign_role(user_id):
    # 分配用户角色
    data = get_json()
    role_ids = data.get("role_ids")
    if not isinstance(role_ids, list) or not all(isinstance(role_id, int) for role_id in role_ids):
        return error_response("角色 ID 必须是整数列表", 400)
    return assign_user_role(user_id, role_ids)
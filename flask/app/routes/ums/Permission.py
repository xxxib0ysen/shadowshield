from flask import Blueprint, request
from app.services.ums.PermissionService import *
from app.utils.response import *

permission_bp = Blueprint("permission", __name__, url_prefix="/permission")

# 添加
@permission_bp.route("/add", methods=["POST"])
def add_permission():
    data = request.json
    return create_permission(data)

# 修改
@permission_bp.route("/edit/<int:permission_id>", methods=["POST"])
def edit_permission(permission_id):
    data = request.json
    return update_permission(permission_id, data)

# 删除
@permission_bp.route("/delete/<int:permission_id>", methods=["POST"])
def remove_permission(permission_id):
    return delete_permission(permission_id)

# 分页查询
@permission_bp.route("/list", methods=["GET"])
def list_permission():
    keyword = request.args.get("keyword", ' ')
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 6, type=int)
    return list_permissions( keyword, page, page_size)

from flask import Blueprint, request
from app.services.ums.RCService import *
from app.utils.response import *

resource_category_bp = Blueprint("resource_category", __name__, url_prefix="/resourceCategory")

# 分页查询
@resource_category_bp.route("/list", methods=["GET"])
def list_category():
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("pageSize", 6, type=int)
    return list_resource_category(page, page_size)

# 添加
@resource_category_bp.route("/add", methods=["POST"])
def add_category():
    data = request.json
    return create_resource_category(data)

# 修改
@resource_category_bp.route("/update/<int:category_id>", methods=["POST"])
def edit_category(category_id):
    data = request.json
    return update_resource_category(category_id, data)

# 删除
@resource_category_bp.route("/delete/<int:category_id>", methods=["POST"])
def delete_category(category_id):
    return delete_resource_category(category_id)

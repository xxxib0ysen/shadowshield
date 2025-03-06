from flask import Blueprint, request
from app.services.ums.ResourceService import *

resource_bp = Blueprint("resource", __name__, url_prefix="/resource")

# 查
@resource_bp.route("/list", methods=["GET"])
def list_all_resource():
    category_id = request.args.get("category_id", type=int)
    name_keyword = request.args.get("name_keyword")
    uri_keyword = request.args.get("uri_keyword")
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("pageSize", 6, type=int)
    return list_resource(category_id, name_keyword, uri_keyword, page, page_size)

# 添加
@resource_bp.route("/add", methods=["POST"])
def add_resource():
    data = request.json
    return create_resource(data)

# 修改
@resource_bp.route("/edit/<int:resource_id>", methods=["POST"])
def edit_resource(resource_id):
    data = request.json
    return update_resource(resource_id, data)

# 删除
@resource_bp.route("/delete/<int:resource_id>", methods=["POST"])
def delete_resource(resource_id):
    return remove_resource(resource_id)



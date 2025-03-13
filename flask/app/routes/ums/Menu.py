from flask import Blueprint, request
from app.services.ums.MenuService import *
from app.utils.response import success_response, error_response

menu_bp = Blueprint('menu', __name__, url_prefix='/menu')

# 添加菜单
@menu_bp.route("/add", methods=["POST"])
def add_menu():
    data = request.json
    return create_menu(data)

# 修改菜单
@menu_bp.route("/edit/<int:menu_id>", methods=["POST"])
def edit_menu(menu_id):
    data = request.json
    return update_menu(menu_id, data)

# 获取所有菜单
@menu_bp.route("/list", methods=["GET"])
def list_menu():
    page = request.args.get("page",1,type=int)
    page_size = request.args.get("page_size",6,type=int)
    level = request.args.get("level", type=int)
    window_key = request.args.get("window_key", type=str)
    return get_all_menu(page,page_size,level,window_key)

# 删除菜单
@menu_bp.route("/delete/<int:menu_id>", methods=["POST"])
def delete_menu(menu_id):
    return remove_menu(menu_id)

# 修改菜单显示状态
@menu_bp.route("/updateHidden/<int:menu_id>", methods=["POST"])
def change_menu_status(menu_id):
    hidden = request.json.get("hidden")
    return update_menu_status(menu_id, hidden)

# 以树形结构返回所有菜单
@menu_bp.route("/treeList", methods=["GET"])
def tree_list():
    window_key = request.args.get("window_key", type=str)
    return get_menu_tree(window_key)



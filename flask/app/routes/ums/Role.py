from flask import  Blueprint, jsonify, request
from app.services.ums.RoleService import *
from app.utils.response import *

role_bp = Blueprint('role', __name__, url_prefix='/role')

# 添加
@role_bp.route('/add', method=['POST'])
def add_role():
    data = request.json
    return create_role(data)

# 编辑
@role_bp.route('/edit/<int:role_id>', methods=['POST'])
def edit_role(role_id):
    data = request.json
    return update_role(role_id, data)

# 删除
@role_bp.route("/delete/<int:role_id>", methods=["POST"])
def delete_role(role_id):
    return remove_role(role_id)


# 模糊分页获取所有
@role_bp.route("/list",methods=["GET"])
def list_role():
    keyword = request.args.get('keyword', ' ')
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get('pageSize', 6, type=int)
    return get_role_list(keyword, page, page_size)

# 启用/禁用
@role_bp.route('/updateStatus/<int:role_id>', methods=['POST'])
def change_status(role_id):
    status = request.json.get("status")
    return update_role_status(role_id, status)

# 获取角色相关菜单
@role_bp.route('/listMenu/<int:role_id>', methods=['GET'])
def role_menu(role_id):
    return get_role_menu(role_id)

# 获取角色相关资源
@role_bp.route('/listResource/<int:role_id>', methods=['GET'])
def role_resource(role_id):
    return get_role_resource(role_id)

# 获取角色数据权限
@role_bp.route('/dataPermission/<int:role_id>', methods=['GET'])
def role_data_permission(role_id):
    return get_role_data_permission(role_id)

# 给角色分配菜单
@role_bp.route('/allocMenu', methods=['POST'])
def allocate_menu():
    data = request.json
    return allocate_role_menu(data.get("role_id"), data.get("menu_ids",[]))

# 给角色分配资源
@role_bp.route('/allocResource', methods=['POST'])
def allocate_resource():
    data = request.json
    return allocate_role_resource(data.get("role_id"), data.get("resource_ids",[]))

# 给角色分配数据权限
@role_bp.route('/allocDataPermission', methods=['POST'])
def allocate_data_permission():
    data = request.json
    return allocate_role_data_permission(data.get("role_id"), data.get("permissions",[]))


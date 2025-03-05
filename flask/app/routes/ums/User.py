from flask import Blueprint,request
from app.services.ums.UserService import *
from app.utils.response import *
from app.utils.common import *

user_bp = Blueprint('user', __name__, url_prefix="/user")

@user_bp.route("/list",methods=["GET"])
# 根据账号或姓名分页获取用户列表
def list_user():
    keyword = request.args.get('keyword', ' ')
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    return get_user_list(keyword, page, page_size)


# 获取指定用户信息
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return get_user_by_id(user_id)

@user_bp.route("/add", methods=["POST"])
def add_user():
    data = request.json
    return create_user(data)

@user_bp.route("/update/<int:user_id>", methods=["POST"])
def edit_user(user_id):
    data = request.json
    return update_user(user_id, data)


@user_bp.route("/delete/<int:user_id>", methods=["POST"])
def remove_user(user_id):
    return delete_user(user_id)

@user_bp.route('/updateStatus/<int:user_id>', methods=['POST'])
def change_status(user_id):
    # 启用/禁用用户
    status = request.json.get('status')
    return update_user_status(user_id, status)

@user_bp.route('/role/update', methods=['POST'])
def update_role():
    # 分配用户角色
    data = request.json
    return assign_role(data.get("user_id"), data.get("role_ids"))

# 获取指定用户的角色
@user_bp.route('/role/<int:user_id>', methods=['GET'])
def get_role(user_id):
    return get_user_role(user_id)
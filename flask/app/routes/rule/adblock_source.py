from flask import Blueprint, request
from app.services.rule.SourceService import SourceService
from app.utils.response import success_response, error_response

adblock_bp = Blueprint('adblock', __name__, url_prefix='/rule/adblock')


#  批量导入
@adblock_bp.route('/add', methods=['POST'])
def add_adblock_source():
    data = request.get_json()
    if not data or "rules" not in data:
        return error_response("请输入有效的规则数据", 400)

    return SourceService.add(data["rules"])


# 分页获取广告规则源
@adblock_bp.route('/list', methods=['get'])
def get_adblock_list():
    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=6, type=int)

    return SourceService.getList(page, page_size)


# 删除
@adblock_bp.route('/delete', methods=['POST'])
def delete_adblock_source():
    data = request.get_json()
    if not data or "source_id" not in data:
        return error_response("请输入有效的 source_id", 400)

    return SourceService.delete(data["source_id"])

# 启用/禁用
@adblock_bp.route('/status', methods=['POST'])
def update_adblock_status():

    data = request.get_json()
    if not data or "source_id" not in data or "status" not in data:
        return error_response("请输入有效的 source_id 和 status", 400)

    return SourceService.update_status(data["source_id"], data["status"])

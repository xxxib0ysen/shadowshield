from flask import Blueprint, request
from app.services.system.SettingService import get_setting, set_setting
from app.utils.response import success_response, error_response

setting_bp = Blueprint("system_setting", __name__, url_prefix="/system")

@setting_bp.route("/getSetting", methods=["GET"])
def get_setting_route():
    key = request.args.get("key")
    if not key:
        return error_response("缺少 key 参数", 400)
    value = get_setting(key)
    return success_response(value, "获取设置成功", 200)

@setting_bp.route("/setSetting", methods=["POST"])
def set_setting_route():
    data = request.get_json()
    key = data.get("key")
    value = data.get("value")
    if not key:
        return error_response("key 不能为空", 400)
    set_setting(key, value)
    return success_response(None, "设置已保存", 200)
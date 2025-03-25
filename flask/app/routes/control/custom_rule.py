from flask import Blueprint, request
from app.services.control.CustomService import (
    get_custom_rules, add_custom_rules, update_custom_rule_status,
    delete_custom_rule, delete_custom_rule_batch
)
from app.utils.response import error_response, success_response

custom_bp = Blueprint("custom_rule", __name__, url_prefix="/custom_rule")

@custom_bp.route("/list", methods=["GET"])
def list_custom_rules():
    return get_custom_rules()

@custom_bp.route("/add", methods=["POST"])
def add_rule():
    data = request.get_json()
    return add_custom_rules(data)

@custom_bp.route("/updateStatus", methods=["POST"])
def update_status():
    data = request.get_json()
    return update_custom_rule_status(data.get("id"), data.get("status"))

@custom_bp.route("/delete", methods=["POST"])
def delete_rule():
    data = request.get_json()
    return delete_custom_rule(data.get("id"))

@custom_bp.route("/batchDelete", methods=["POST"])
def batch_delete():
    data = request.get_json()
    return delete_custom_rule_batch(data.get("ids", []))


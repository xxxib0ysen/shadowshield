from flask import jsonify

def success_response(data=None, message="请求成功", code=200):
    """
    成功响应
    :param data: 返回的数据
    :param message: 提示信息
    :param code: 状态码
    :return: JSON响应
    """
    response = {
        "code": code,
        "message": message,
        "data": data
    }
    return jsonify(response), code

def error_response(message="请求失败", code=400,data=None):
    """
    错误响应
    :param message: 错误消息
    :param code: 状态码
     param data: 可选的错误数据
    :return: JSON 响应
    """
    response = {
        "code": code,
        "message": message,
        "data": data
    }
    return jsonify(response), code
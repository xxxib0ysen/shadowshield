from flask import request

def get_json():
    # 获取请求中的 JSON 数据
    try:
        return request.get_json()
    except Exception:
        return None

def validate_params(required_params, data):
    """
    验证请求参数是否完整
    :param required_params: 必填参数列表
    :param data: 请求数据
    :return: 缺失参数列表
    """
    missing_params = [param for param in required_params if param not in data]
    return missing_params
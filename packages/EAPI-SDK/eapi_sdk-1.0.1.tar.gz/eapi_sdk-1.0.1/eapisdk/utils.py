import os
import json
from datetime import datetime
from typing import Union

# 示例：获取当前时间戳
def get_current_timestamp():
    return datetime.utcnow().timestamp()

# 示例：将字典转换为JSON字符串并美化输出
def to_pretty_json(data: dict) -> str:
    return json.dumps(data, indent=4, ensure_ascii=False)

# 示例：从环境变量获取API密钥和访问密钥
def get_credentials_from_env():
    access_key = os.environ.get("OPENAPI_ACCESS_KEY")
    secret_key = os.environ.get("OPENAPI_SECRET_KEY")

    if not (access_key and secret_key):
        raise ValueError("请确保已设置OPENAPI_ACCESS_KEY和OPENAPI_SECRET_KEY环境变量")

    return access_key, secret_key

# 示例：处理API响应结果
def handle_api_response(response: Union[dict, list]):
    if "error" in response:
        error_data = response["error"]
        raise ErrorResponse(error_code=error_data["code"], message=error_data["message"])

    return response

# 示例：检查HTTP响应的状态码是否成功
def is_successful_response(response: requests.Response) -> bool:
    return 200 <= response.status_code < 300

# ... 更多根据实际需求编写的工具函数
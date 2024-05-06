import json

import requests
from requests.auth import HTTPBasicAuth
from typing import Dict, Any
import hashlib
import time


class EAPIClient:
    def __init__(self, access_key: str, secret_key: str, base_url='http://121.40.232.157:8090/api/interfaceInfo/invoke'):
        """
        初始化OpenAPI客户端
        :param access_key: OpenAPI平台的Access Key
        :param secret_key: OpenAPI平台的Secret Key
        :param base_url: OpenAPI平台的基础URL，默认值为'部署后的url'
        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.base_url = base_url
        self.auth = HTTPBasicAuth(self.access_key, self.secret_key)

    def _make_request(self, method: str, interfaceInfoId: int, json_payload: Dict[str, Any] = None):
        id = interfaceInfoId
        """
        发送HTTP请求到指定的OpenAPI接口
        :param method: 请求方法，例如 'GET', 'POST', 'PUT', 'DELETE' 等
        :param endpoint: 接口路径，相对于base_url
        :param interfaceInfoId: 接口id
        :param json_payload: JSON格式的请求体
        :return: 响应的JSON数据
        """
        timestamp_in_seconds = int(time.time())
        timestamp_string = str(timestamp_in_seconds)
        # 拼接字符串：时间戳 + "." + secretKey
        to_sign = timestamp_string + "." + self.secret_key

        # 使用MD5对拼接后的字符串进行加密
        md5_hash = hashlib.md5(to_sign.encode('utf-8'))

        # 获取MD5加密后的十六进制字符串，这就是所需的sign
        sign = md5_hash.hexdigest()
        headers = {
            'Content-Type': 'application/json',
            'sign': sign,  # 假设此处留空或后续填充具体签名值
            'timeStamp': timestamp_string,  # 假设此处留空或后续填充具体时间戳值
            'accessKey': self.access_key,
            'nonce': str(85),  # 将整数转换为字符串，通常HTTP头中的值应为字符串
            'interfaceInfoId': str(id),
        }
        json_finload = {
            'id': id,
            'userRequestParams': json_payload
        }
        if json_payload is not None:
            response = requests.post(self.base_url, json=json_finload, headers=headers, verify=False)
            return response.json().get("data")
        else:
            response = requests.request(method, self.base_url, auth=self.auth, headers=headers)
            return response
    def call_api(self, params: Dict[str, Any], interfaceInfoId: int, method: str = 'POST'):
        """
        根据接口名称调用OpenAPI接口
        :param interfaceInfoId: 接口id
        :param interfaceInfoId:
        :param params: JSON格式的请求参数
        :param method: HTTP请求方法，默认为'POST'
        :return: 响应的JSON数据
        """
        # 假设接口路径是固定的，可以根据实际情况调整
        # 替换为实际的接口版本和接口路径
        return self._make_request(method, interfaceInfoId, params)

# 示例：调用名为'get_user_info'的接口
# client = OpenAPIClient('your_access_key', 'your_secret_key')
# user_info = client.call_api('get_user_info', {'user_id': '123'})

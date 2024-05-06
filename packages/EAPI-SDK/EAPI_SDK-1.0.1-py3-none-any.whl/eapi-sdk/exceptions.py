class OpenAPIException(Exception):
    """
    OpenAPI接口调用异常基类
    """
    pass


class AuthenticationError(OpenAPIException):
    def __init__(self, message: str = "认证失败，请检查Access Key和Secret Key是否正确",
                 response: Optional[requests.Response] = None):
        self.message = message
        self.status_code: Optional[int] = None
        self.error_details: Optional[Union[dict, str]] = None

        if response is not None:
            self.status_code = response.status_code
            try:
                self.error_details = response.json()
            except json.JSONDecodeError:
                self.error_details = response.text

        super().__init__(self.message)

    def __str__(self):
        if self.response is not None:
            return f"{self.message}, HTTP状态码: {self.status_code}, 错误详情: {self.error_details}"
        else:
            return self.message


class RequestFailed(OpenAPIException):
    """
    请求失败异常，如HTTP状态码非200系列
    """
    def __init__(self, status_code: int, message: str, response_body: dict):
        super().__init__(f"请求失败，状态码：{status_code}，消息：{message}")
        self.status_code = status_code
        self.message = message
        self.response_body = response_body


class InvalidResponseFormat(OpenAPIException):
    """
    响应格式错误异常，比如无法解析JSON响应
    """
    pass

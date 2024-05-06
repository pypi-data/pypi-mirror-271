from client import EAPIClient


# 创建默认的客户端
def create_client(access_key, secret_key,
                  base_url):  # baseUrl要改成部署后的网关
    client = EAPIClient(access_key, secret_key, base_url)
    return client.call_api({"question": "你好"}, 3)

create_client ("f4c35007d12293c95c15bfd62e39b90a", "6843da9900c6fa8961bc330128768f7f","http://121.40.232.157:8090/api/interfaceInfo/invoke")


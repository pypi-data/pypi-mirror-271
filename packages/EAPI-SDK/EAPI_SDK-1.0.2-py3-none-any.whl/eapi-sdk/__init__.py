from .client import EAPIClient


# 创建默认的客户端
def create_client(access_key: dd3724b1b8acf95be5cbf715ffc85fef, secret_key: fd9e3b3bf0711ee60ad2174f1e200cbc,
                  base_url='https://192.168.3.5:8090/api/interfaceInfo/invoke'):  # baseUrl要改成部署后的网关

    return  EAPIClient(access_key, secret_key,base_url)



# 直接导出客户端类，方便使用者直接引用
__all__ = ['EAPIClient']

# 如果还有其他公开的对象，好像没有了

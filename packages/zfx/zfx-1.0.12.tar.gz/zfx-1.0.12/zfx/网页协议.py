import requests

def 网页协议_发送_GET请求(网址, 参数=None):
    """
    发送 GET 请求并返回服务器响应对象
    :param 网址: 请求的 URL
    :param 参数: 要发送的参数，字典形式，默认为 None
    :return: 服务器响应对象，如果请求失败则返回 None
    """
    try:
        响应 = requests.get(网址, params=参数)
        return 响应
    except Exception as e:
        print("GET 请求发生异常:", e)
        return None


def 网页协议_发送_POST请求(网址, 数据):
    """
    发送 POST 请求并返回服务器响应
    :param 网址: 请求的 URL
    :param 数据: 要发送的数据，字典形式
    :return: 服务器响应的文本，如果请求失败则返回空字符串
    """
    try:
        响应 = requests.post(网址, data=数据)
        return 响应.text
    except Exception as e:
        print("POST 请求发生异常:", e)
        return ''


def 网页协议_获取_HTTP状态码(响应):
    """
    获取 HTTP 状态码
    :param 响应: 服务器响应对象
    :return: HTTP 状态码，如果响应为 None 则返回 None
    """
    if 响应 is not None:
        return 响应.status_code
    else:
        return None


def 网页协议_获取_响应文本(响应):
    """
    获取响应的文本内容
    :param 响应: 服务器响应对象
    :return: 响应的文本内容，如果响应为 None 则返回空字符串
    """
    if 响应 is not None:
        return 响应.text
    else:
        return ''


def 网页协议_获取_响应二进制内容(响应):
    """
    获取响应的二进制内容
    :param 响应: 服务器响应对象
    :return: 响应的二进制内容，如果响应为 None 则返回空字节串
    """
    if 响应 is not None:
        return 响应.content
    else:
        return b''


def 网页协议_获取_响应头(响应):
    """
    获取响应头的字典形式
    :param 响应: 服务器响应对象
    :return: 响应头的字典形式，如果响应为 None 则返回空字典
    """
    if 响应 is not None:
        return 响应.headers
    else:
        return {}


def 网页协议_获取_响应URL(响应):
    """
    获取响应的 URL
    :param 响应: 服务器响应对象
    :return: 响应的 URL，如果响应为 None 则返回空字符串
    """
    if 响应 is not None:
        return 响应.url
    else:
        return ''


def 网页协议_获取_响应编码(响应):
    """
    获取响应的编码格式
    :param 响应: 服务器响应对象
    :return: 响应的编码格式，如果响应为 None 则返回空字符串
    """
    if 响应 is not None:
        return 响应.encoding
    else:
        return ''


def 网页协议_获取_响应cookies(响应):
    """
    获取响应的 cookies
    :param 响应: 服务器响应对象
    :return: 响应的 cookies，如果响应为 None 则返回空字典
    """
    if 响应 is not None:
        return 响应.cookies
    else:
        return {}
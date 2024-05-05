import hashlib


def 系统_取硬盘特征字():
    """
    # 调用函数来获取系统硬盘特征字,获取失败则返回空
    disk_feature = 系统_取硬盘特征字()
    print("系统硬盘特征字:", disk_feature)
    """
    try:
        # 以二进制形式读取已知存在的文件，例如 C:\Windows\explorer.exe
        with open('C:\\Windows\\explorer.exe', 'rb') as f:
            # 读取前 4096 字节
            data = f.read(4096)
        # 计算数据的 MD5 哈希值
        hash_value = hashlib.md5(data).hexdigest()
        # 将哈希值转换为整数
        feature_code = int(hash_value, 16)
        return feature_code
    except Exception as e:
        print("获取系统硬盘特征字时出错:", e)
        return None
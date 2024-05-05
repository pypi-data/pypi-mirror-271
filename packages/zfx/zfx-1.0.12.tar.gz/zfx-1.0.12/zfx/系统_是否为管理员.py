import ctypes


def 系统_是否为管理员():
    """
    # 调用函数来检查管理员权限,返回True则为管理，返回False则为普通用户
    系统_是否为管理员():
    """
    try:
        # 使用Windows API来检查当前进程是否以管理员权限运行
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as e:
        print("检查管理员权限时出错:", e)
        return False
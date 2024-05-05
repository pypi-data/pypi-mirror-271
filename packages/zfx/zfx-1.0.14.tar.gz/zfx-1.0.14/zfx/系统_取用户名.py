import getpass


def 系统_取用户名():
    """
    # 调用函数来获取系统用户名,无需传递任何参数，获取失败返回空
    current_username = 系统_取用户名()
    print("当前系统用户名:", current_username)
    """
    try:
        username = getpass.getuser()
        return username
    except Exception as e:
        print("获取系统用户名时出错:", e)
        return None
import datetime


def 系统_取时区():
    """
    # 调用函数来获取系统时区,获取成功将正常返回，获取失败则返回空
    timezone = 系统_取时区()
    print("系统时区:", timezone)
    """
    try:
        # 获取当前日期时间对象
        current_time = datetime.datetime.now()
        # 获取当前时区信息
        timezone_info = current_time.astimezone().tzinfo
        # 格式化时区信息为字符串
        timezone_str = str(timezone_info)
        return timezone_str
    except Exception:
        return None

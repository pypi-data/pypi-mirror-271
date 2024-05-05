import datetime


def 系统_取系统现行时间():
    """
    获取系统当前时间。无需传递参数
    """
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

import platform

def 系统_取CPU型号() -> str:
    """
    # 示例用法 获取电脑CPU型号，无需传递参数。直接返回CPU信息
    cpu型号 = 系统_取CPU型号()
    print("CPU型号：", cpu型号)
    """
    return platform.processor()



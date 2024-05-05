import os


def 系统_强制重启():
    """
    # 在 Windows 上使用命令 "shutdown /r /f /t 0" 来强制重启
    # 调用函数来进行强制重启
    系统_强制重启()
    """
    os.system("shutdown /r /f /t 0")

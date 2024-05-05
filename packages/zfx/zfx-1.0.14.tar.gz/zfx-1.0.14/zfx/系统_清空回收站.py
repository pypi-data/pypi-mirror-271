import ctypes


def 系统_清空回收站():
    """
    # 定义回收站清空标志
    # 调用函数来清空回收站,无需传递任何参数
    # 系统_清空回收站()
    """
    SHERB_NOCONFIRMATION = 0x00000001
    SHERB_NOPROGRESSUI = 0x00000004
    # 设置标志为直接清空
    flags = SHERB_NOCONFIRMATION | SHERB_NOPROGRESSUI
    # 使用 SHEmptyRecycleBin 函数清空回收站
    ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, flags)



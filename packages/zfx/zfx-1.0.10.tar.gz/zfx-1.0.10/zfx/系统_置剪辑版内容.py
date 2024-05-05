import pyperclip


def 系统_置剪辑版内容(参数):
    # 将文本内容复制到系统的剪辑版内，相当于Ctrl+C的效果
    pyperclip.copy(str(参数))

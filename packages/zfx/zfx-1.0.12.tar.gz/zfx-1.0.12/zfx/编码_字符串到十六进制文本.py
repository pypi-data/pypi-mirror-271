def 编码_字符串到十六进制文本(text):
    """
    将字符串转换为16进制文本
    text = "Hello, World!"
    hex_text = 字符串转16进制文本(text)
    print("字符串转换为16进制文本:", hex_text)
    """
    byte_text = text.encode()
    hex_text = ' '.join([hex(byte)[2:].zfill(2) for byte in byte_text])
    return hex_text




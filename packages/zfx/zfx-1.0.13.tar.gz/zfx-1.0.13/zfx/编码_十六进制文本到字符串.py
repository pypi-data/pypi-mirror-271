def 编码_十六进制文本到字符串(hex_text):
    """
    将16进制文本转换为字符串
    converted_text = 十六进制文本转字符串("48 65 6c 6c 6f 2c 20 57 6f 72 6c 64 21")
    print("16进制文本转换为字符串:", converted_text)
    """
    byte_text = bytes.fromhex(hex_text.replace(' ', ''))
    text = byte_text.decode()
    return text




import os


def 目录_创建(目录路径):
    """
    # 使用示例，成功返回 True 失败返回 False
    目录_创建("C:/哈哈/哈哈哈")
    """
    try:
        os.makedirs(目录路径, exist_ok=True)
        return True
    except Exception as e:
        print(f"An error occurred while creating directory: {e}")
        return False
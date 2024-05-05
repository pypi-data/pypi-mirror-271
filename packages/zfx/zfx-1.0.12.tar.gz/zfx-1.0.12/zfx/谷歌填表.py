from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def 谷歌填表_初始化(chrome驱动路径, 浏览器路径, 启动参数=[]):
    """
    将返回一个驱动对象，用于后续的浏览器操作。
    # 使用示例
    # chrome驱动路径 = "C:\\Users\\Administrator\\Desktop\\chrome-win64\\chromedriver.exe"
    # 浏览器路径 = "C:\\Users\\Administrator\\Desktop\\chrome-win64\\chrome.exe"
    # 启动参数 = ["--incognito", "--disable-gpu"]  # 添加启动参数
    # driver = 谷歌填表_初始化(chrome驱动路径, 浏览器路径, 启动参数)
    """
    # 创建 ChromeDriver 服务对象
    chrome服务 = Service(chrome驱动路径)

    # 启动 ChromeDriver 服务
    chrome服务.start()

    # 创建 Chrome 驱动器对象并指定服务
    选项 = webdriver.ChromeOptions()
    选项.binary_location = 浏览器路径

    # 添加启动参数
    for 参数 in 启动参数:
        选项.add_argument(参数)

    驱动器 = webdriver.Chrome(service=chrome服务, options=选项)

    return 驱动器


def 谷歌填表_访问网页(参_driver, 网址):
    """
    使用提供的驱动程序访问指定的网址。

    Args:
        参_driver: WebDriver 对象，用于控制浏览器的行为。
        网址: 要访问的网址。

    Returns:
        无
    """
    参_driver.get(网址)



def 谷歌填表_置浏览器大小和位置(参_driver, 宽度, 高度, x_位置, y_位置):
    """
    设置浏览器窗口的大小和位置。
    参数:
        驱动器: WebDriver 对象，表示浏览器驱动器。
        宽度: int，表示窗口宽度（像素）。
        高度: int，表示窗口高度（像素）。
        x_位置: int，表示窗口左上角的 x 坐标位置。
        y_位置: int，表示窗口左上角的 y 坐标位置。
    """
    参_driver.set_window_size(宽度, 高度)
    参_driver.set_window_position(x_位置, y_位置)


def 谷歌填表_后退(参_driver):
    """
    使用提供的驱动程序执行后退操作。

    Args:
        参_driver: WebDriver 对象，用于控制浏览器的行为。

    Returns:
        无
    """
    参_driver.back()


def 谷歌填表_前进(参_driver):
    """
    使用提供的驱动程序执行前进操作。

    Args:
        参_driver: WebDriver 对象，用于控制浏览器的行为。

    Returns:
        无
    """
    参_driver.forward()


def 谷歌填表_刷新(参_driver):
    """
    使用提供的驱动程序执行刷新操作。

    Args:
        参_driver: WebDriver 对象，用于控制浏览器的行为。

    Returns:
        无
    """
    参_driver.refresh()



def 谷歌填表_查找元素(参_driver, by, value):
    """
    driver: WebDriver 对象，即浏览器驱动器，用于在网页上执行操作。
    by: 定位方法，指定如何定位元素，可以是 "id"、"name"、"class_name"、"xpath" 等。
    value: 定位值，根据定位方法指定的方式，传入相应的定位值。
    返回 查找到的第一个元素
    """
    return 参_driver.find_element(by=by, value=value)


def 谷歌填表_查找多个元素(参_driver, by, value):
    """
        driver: WebDriver 对象，即浏览器驱动器，用于在网页上执行操作。
        by: 定位方法，指定如何定位元素，可以是 "id"、"name"、"class_name"、"xpath" 等。
        value: 定位值，根据定位方法指定的方式，传入相应的定位值。
        返回 查找到的所有元素
    """
    return 参_driver.find_elements(by=by, value=value)


def 谷歌填表_点击元素(元素):
    元素.click()


def 谷歌填表_输入文本(元素, 文本):
    元素.send_keys(文本)


def 谷歌填表_清除文本(元素):
    元素.clear()


def 谷歌填表_获取属性值(元素, 属性名):
    return 元素.get_attribute(属性名)


def 谷歌填表_判断可见(元素):
    return 元素.is_displayed()


def 谷歌填表_判断可用(元素):
    return 元素.is_enabled()


def 谷歌填表_判断选中(元素):
    return 元素.is_selected()


def 谷歌填表_等待元素出现(参_driver, 定位方法, 定位值, 超时时间=10):
    return WebDriverWait(参_driver, 超时时间).until(EC.presence_of_element_located((定位方法, 定位值)))


def 谷歌填表_等待元素可见(参_driver, 定位方法, 定位值, 超时时间=10):
    return WebDriverWait(参_driver, 超时时间).until(EC.visibility_of_element_located((定位方法, 定位值)))


def 谷歌填表_等待元素可点击(参_driver, 定位方法, 定位值, 超时时间=10):
    return WebDriverWait(参_driver, 超时时间).until(EC.element_to_be_clickable((定位方法, 定位值)))


def 谷歌填表_执行JavaScript(参_driver, 脚本, *参数):
    return 参_driver.execute_script(脚本, *参数)


def 谷歌填表_切换窗口(参_driver, 窗口名称):
    参_driver.switch_to.window(窗口名称)


def 谷歌填表_切换框架(参_driver, 框架引用):
    参_driver.switch_to.frame(框架引用)


def 谷歌填表_保存截图(参_driver, 文件名):
    参_driver.save_screenshot(文件名)


def 谷歌填表_获取页面源代码(参_driver):
    return 参_driver.page_source


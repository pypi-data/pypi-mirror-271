# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  web-ui-helper
# FileName:     browser.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/04/29
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import os
import time
import base64
import ddddocr
import requests
import selenium
from PIL import Image
from io import BytesIO
from selenium import webdriver
from abc import abstractmethod
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from seleniumwire import webdriver as driver_wire
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
# expected_conditions 类负责条件
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.firefox.webdriver import WebDriver as Firefox
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from web_ui_helper.common.log import logger
from web_ui_helper.common.webdriver import Locator
from web_ui_helper.common.date_extend import get_current_datetime_int_str
from web_ui_helper.decorators.selenium_exception import element_find_exception, loop_find_element
from web_ui_helper.common.dir import get_project_path, get_chrome_default_user_data_path, get_var_path, is_file, \
    get_browser_bin_exe, create_directory, move_file, is_dir, get_browser_process_name, is_process_running


class Browser(object):
    TIMEOUT = 10
    LOG_LEVEL = "DEBUG"
    BROWSER_NAME = None
    LOG_PATH = os.path.join(get_project_path(), "log")
    create_directory(LOG_PATH)
    BIN_PATH = os.path.join(get_project_path(), "bin")
    create_directory(BIN_PATH)
    USERDATA_PATH = None
    IMAGE_PATH = os.path.join(get_project_path(), "image")
    create_directory(IMAGE_PATH)

    def __init__(self, browser_path: str, is_headless: bool, proxy_address: str) -> None:
        self.browser_path = browser_path
        self.is_headless = is_headless
        self.proxy_address = proxy_address

    @abstractmethod
    def get_browser(self):
        pass

    @classmethod
    def get_options(cls):
        pass

    @abstractmethod
    def get_service(self):
        pass

    @abstractmethod
    def is_running(self):
        pass


class ChromeBrowser(Browser):
    BROWSER_NAME = "Chrome"

    def __init__(self, browser_path: str, is_headless: bool, proxy_address: str) -> None:
        super().__init__(browser_path, is_headless, proxy_address)
        self.driver_file = os.path.join(self.BIN_PATH, "chromedriver.exe")
        if is_file(self.driver_file) is False:
            logger.warning("开始下载与浏览器版本匹配的chromedriver.exe文件.")
            # 自动下载并安装适用于当前 Chrome 版本的 chromedriver
            driver_path = ChromeDriverManager().install()
            move_file(src_file=driver_path, dst_path=self.BIN_PATH)
            logger.warning("chromedriver.exe文件下载完成.")
        self.__bind_chrome_user_data_dir()

    def __bind_chrome_user_data_dir(self) -> None:
        self.USERDATA_PATH = get_chrome_default_user_data_path()
        if is_dir(self.USERDATA_PATH) is False:
            self.USERDATA_PATH = os.path.sep.join([os.getcwd(), "profile", "chrome-profile"])
            create_directory(self.USERDATA_PATH)
        logger.warning("浏览器用户的数据目录为: {}".format(self.USERDATA_PATH))

    def get_options(self) -> Options:
        # 支持的浏览器有: Firefox, Chrome, Ie, Edge, Opera, Safari, BlackBerry, Android, PhantomJS等
        chrome_options = driver_wire.ChromeOptions()
        # 谷歌文档提到需要加上这个属性来规避bug
        chrome_options.add_argument('--disable-gpu')
        # 隐身模式（无痕模式）
        # chrome_options.add_argument('--incognito')
        # 隐藏"Chrome正在受到自动软件的控制"
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument('--user-data-dir={}'.format(self.USERDATA_PATH))
        # chrome_options.add_argument("--disable-autofill-passwords")  # 禁用自动填充密码
        # chrome_options.add_argument("--disable-save-password-bubble")  # 禁用保存密码提示框
        # 设置中文
        # chrome_options.add_argument('lang=zh_CN.UTF-8')
        # chrome_options.add_argument('--no-sandbox')  # linux下
        if self.is_headless is True:
            # 谷歌浏览器后台运行模式
            chrome_options.add_argument('--headless')
            # 指定浏览器分辨率
            chrome_options.add_argument('--window-size=1920,1080')
        else:
            # 浏览器最大化
            chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # 或者使用下面的设置, 提升速度
        # chrome_options.add_argument('blink-settings=imagesEnabled=false')
        # 隐藏滚动条, 应对一些特殊页面
        # chrome_options.add_argument('--hide-scrollbars')
        # chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.add_argument('--log-level=3')
        # 手动指定使用的浏览器位置，如果谷歌浏览器的安装目录配置在系统的path环境变量中，那么此处可以不传路径
        logger.warning("当前系统Chrome浏览器可运行程序的路径为：{}".format(self.browser_path))
        chrome_options.binary_location = self.browser_path
        # 添加代理设置到 Chrome 选项
        logger.warning("使用代理地址：{}".format(self.proxy_address or "null"))
        if self.proxy_address:
            chrome_options.add_argument('--proxy-server=http://{}'.format(self.proxy_address))
            chrome_options.add_argument('--proxy-server=https://{}'.format(self.proxy_address))
        pre = dict()
        # 设置这两个参数就可以避免密码提示框的弹出
        pre["credentials_enable_service"] = False
        pre["profile.password_manager_enabled"] = False
        # pre["profile.default_content_settings.popups"] = 0
        # 禁止加载图片
        # pre["profile.managed_default_content_settings.images"] = 2
        chrome_options.add_experimental_option("prefs", pre)
        chrome_options.add_experimental_option('useAutomationExtension', False)
        # 关闭devtools工具,
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        return chrome_options

    def get_service(self) -> ChromeService:
        # 指定chrome_driver路径
        # chrome_driver = r"C:\Python\spiderStudyProject\driver\chromedriver.exe"
        # 指定chrome_driver记录的日志信息
        log_file = os.path.join(self.LOG_PATH, "chrome.log")
        # 如果selenium的版本高于4.6，则不需要配置executable_path参数
        # 指定chrome_driver记录的日志信息
        logger.warning("ChromedDriver路径：{}".format(self.driver_file))
        service = ChromeService(
            executable_path=self.driver_file,
            service_args=['--log-level={}'.format(self.LOG_LEVEL), '--append-log', '--readable-timestamp'],
            log_output=log_file
        )
        return service

    def get_browser(self) -> tuple:
        service = self.get_service()
        options = self.get_options()
        browser = Chrome(service=service, options=options)
        logger.warning("Selenium 版本: {}".format(selenium.__version__))
        logger.warning("浏览器版本: {}".format(browser.capabilities['browserVersion']))
        # 设置隐式等待时间为3秒
        # browser.implicitly_wait(3)
        # 反屏蔽
        browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})',
        })
        wait = WebDriverWait(driver=browser, timeout=self.TIMEOUT)
        return browser, wait, self.BROWSER_NAME

    def is_running(self) -> bool:
        process_name = get_browser_process_name(self.BROWSER_NAME)
        return is_process_running(process_name=process_name)


class FirefoxBrowser(Browser):
    BROWSER_NAME = "Firefox"

    def __init__(self, browser_path: str, is_headless: bool, proxy_address: str) -> None:
        super().__init__(browser_path, is_headless, proxy_address)

    def get_options(self) -> FirefoxOptions:
        firefox_profile = FirefoxOptions()
        # 在无头模式下运行 Firefox
        firefox_profile.headless = self.is_headless
        # 设置代理
        # options.add_argument('--proxy-server=http://proxy.example.com:8080')
        logger.warning("获取的浏览器可运行文件路径为：{}".format(self.browser_path))
        firefox_profile.binary_location = self.browser_path
        # 禁止浏览器自动填充账号，密码
        firefox_profile.set_preference('signon.autofillForms', False)  # 禁止自动填充表单
        firefox_profile.set_preference('signon.autologin.proxy', False)
        firefox_profile.set_preference("signon.rememberSignons", False)  # 不保存密码
        firefox_profile.set_preference('signon.storeWhenAutocompleteOff', False)
        return firefox_profile

    @classmethod
    def get_service(cls) -> FirefoxService:
        # geckodriver 驱动路径
        # gecko_driver_path = '/path/to/geckodriver'
        # 指定gecko_driver记录的日志信息
        log_file = os.path.join(cls.LOG_PATH, "firefox.log")
        # 如果selenium的版本高于4.6，则不需要配置executable_path参数
        service = FirefoxService(
            # executable_path=gecko_driver_path,
            service_args=['--log={}'.format(cls.LOG_LEVEL.lower())],
            log_output=log_file
        )
        return service

    def get_browser(self) -> tuple:
        options = self.get_options()
        service = self.get_service()
        browser = Firefox(service=service, options=options)
        # 设置隐式等待时间为3秒
        # browser.implicitly_wait(3)
        wait = WebDriverWait(driver=browser, timeout=self.TIMEOUT)
        return browser, wait, self.BROWSER_NAME

    def is_running(self) -> bool:
        process_name = get_browser_process_name(self.BROWSER_NAME)
        return is_process_running(process_name=process_name)


class SeleniumProxy(object):

    def __init__(self, browser_name: str, proxy_address: str, browser_path: str = None,
                 is_headless: bool = False) -> None:
        if browser_path:
            if not is_file(browser_path):
                raise ValueError("browser path is not exist")
        else:
            browser_path = get_var_path(var=browser_name)
            if not browser_path:
                raise ValueError("system not installed {} browser.".format(browser_name))
        exe_name = get_browser_bin_exe(browser_name=browser_name)
        exe_file = os.path.join(browser_path, exe_name)
        if browser_name == "Chrome":
            self.browser_proxy = ChromeBrowser(browser_path=exe_file, is_headless=is_headless,
                                               proxy_address=proxy_address)
            if self.browser_proxy.is_running() is True:
                raise ValueError("Chrome browser is already running.")
            self.browser, self.wait, self.browser_name = self.browser_proxy.get_browser()
        elif browser_name == "Firefox":
            self.browser_proxy = FirefoxBrowser(browser_path=exe_file, is_headless=is_headless,
                                                proxy_address=proxy_address)
            if self.browser_proxy.is_running() is True:
                raise ValueError("Firefox browser is already running.")
            self.browser, self.wait, self.browser_name = self.browser_proxy.get_browser()
        else:
            raise ValueError("Browser name must be Chrome or Firefox.")

    def input_text(self, selector: str, regx: str, value: str) -> bool:
        """
        selector 选择器
        regx 选择器所要匹配的表达式
        value 文本框输入值
        """
        flag = False
        try:
            input_1 = self.wait.until(
                ec.presence_of_element_located((Locator.get(selector), regx))
            )
            # 模拟键盘操作清空输入框内容
            input_1.send_keys(Keys.CONTROL + "a")  # 选中输入框中的所有内容
            input_1.send_keys(Keys.BACKSPACE)  # 删除选中的内容
            # 判断输入框是否有数据
            # if input_1.get_attribute("value"):
            # 清除存在的值
            # input_1.clear()
            # 使用 JavaScript 清除输入框的内容
            # self.browser.execute_script("arguments[0].setAttribute('value', '')", input_1)
            input_1.send_keys('{}'.format(value))
            flag = True
        except Exception as e:
            err_str = "通过选择器：{}，表达式: {}，捕获输入框设置文本<{}>失败，error：{}".format(selector, regx, value, e)
            logger.error(err_str)
        return flag

    def submit_click(self, selector: str, regx: str) -> bool:
        """
        selector 选择器
        regx 选择器所要匹配的表达式
        value 文本框输入值
        """
        flag = False
        try:
            submit = self.wait.until(
                ec.element_to_be_clickable((Locator.get(selector), regx))
            )
            submit.click()
            flag = True
        except Exception as e:
            err_str = "通过选择器：{}，表达式: {}，捕获点击对象并点击失败，error：{}".format(selector, regx, e)
            logger.error(err_str)
        return flag

    def get_code(self, selector: str, regx: str) -> str:
        logger.warning("开始获取验证码...")
        ocr_result = None
        try:
            selector = Locator.get(selector)
            captcha = self.browser.find_element(Locator.get(selector), regx)
            code_image = Image.open(BytesIO(captcha.screenshot_as_png))
            # 1.初始化一个实例，配置识别模式默认为OCR识别
            ocr = ddddocr.DdddOcr(show_ad=False)
            ocr_result = ocr.classification(code_image)
            logger.warning("识别到的验证码为：", ocr_result)
            return ocr_result
        except Exception as e:
            err_str = "通过选择器：{}，表达式: {}，识别验证码失败，error：{}".format(selector, regx, e)
            logger.error(err_str)
        return ocr_result

    def alert_accept(self) -> bool:
        # 等待弹框出现
        try:
            alert = self.wait.until(ec.alert_is_present())
            logger.warning("弹框已出现")
            # 处理弹框，点击确定按钮
            alert.accept()
        except (Exception,):
            logger.warning("未出现弹框，无需处理。")
        return True

    def get_element_text(self, selector: str, regx: str) -> str:
        element_text = None
        try:
            # 根据实际情况定位按钮元素
            element = self.browser.find_element(Locator.get(selector), regx)
            # 获取按钮元素的文本信息
            element_text = element.text.strip() if isinstance(element.text, str) else ""
            logger.warning("获取元素的文字信息为: {}".format(element_text))
            return element_text
        except Exception as e:
            err_str = "通过选择器：{}，表达式: {}，获取元素文本信息失败，error：{}".format(selector, regx, e)
            logger.error(err_str)
        return element_text

    def get_element(self, selector: str, regx: str) -> WebElement:
        element = None
        try:
            # 根据实际情况定位按钮元素
            element = self.browser.find_element(Locator.get(selector), regx)
        except (NoSuchElementException,):
            err_str = "通过选择器：{}，表达式: {}，没有找到对应的元素".format(selector, regx)
            logger.warning(err_str)
        except Exception as e:
            err_str = "通过选择器：{}，表达式: {}，获取元素失败，error：{}".format(selector, regx, e)
            logger.error(err_str)
        return element

    def get_elements(self, selector: str, regx: str) -> [WebElement]:
        elements = list()
        try:
            # 根据实际情况定位按钮元素
            elements = self.browser.find_elements(Locator.get(selector), regx)
        except (NoSuchElementException,):
            err_str = "通过选择器：{}，表达式: {}，没有找到对应的元素".format(selector, regx)
            logger.warning(err_str)
        except Exception as e:
            err_str = "通过选择器：{}，表达式: {}，获取元素失败，error：{}".format(selector, regx, e)
            logger.error(err_str)
        return elements

    def get_background_color(self, selector: str, regx: str) -> str:
        background_color = None
        try:
            # 根据实际情况定位按钮元素
            element = self.browser.find_element(Locator.get(selector), regx)
            # 获取选项的背景颜色
            background_color = element.value_of_css_property("background-color")
            background_color = background_color.strip() if isinstance(background_color, str) else ""
        except Exception as e:
            err_str = "通过选择器：{}，表达式: {}，获取背景颜色失败，error：{}".format(selector, regx, e)
            logger.error(err_str)
        return background_color

    def quit(self) -> None:
        self.browser.quit()

    def get(self, url: str) -> None:
        self.browser.get(url)

    def get_current_url(self) -> str:
        return self.browser.current_url

    def get_image_raw(self, locator: str, regx: str, code: str = "base64", filename: str = None) -> str:
        image_name = None
        try:
            # 定位图片元素
            image = self.wait.until(
                ec.presence_of_element_located((Locator.get(locator), regx))
            )
            # 获取图片的 src 属性
            img_src = image.get_attribute("src")
            if code == "base64":
                img_data = base64.b64decode(img_src.split('base64,')[-1].strip(""))
            else:
                # 下载图片并保存
                response = requests.get(img_src)
                img_data = response.content
            img = Image.open(BytesIO(img_data))
            suffix = get_current_datetime_int_str()
            if filename:
                filename = "{}_{}.png".format(filename, suffix)
            else:
                filename = "image_{}.png".format(suffix)
            image_name = os.path.sep.join([self.browser_proxy.IMAGE_PATH, filename])
            # 保存图片到本地文件
            img.save(image_name)
        except Exception as e:
            err_str = "通过选择器：{}，表达式: {}，获取原始图片失败，error：{}".format(locator, regx, e)
            logger.error(err_str)
        return image_name

    def is_exist_element(self, locator: str, regx: str) -> bool:
        is_exist = False
        try:
            # 根据实际情况定位按钮元素
            element = self.browser.find_element(Locator.get(locator), regx)
            if element:
                is_exist = True
        except (NoSuchElementException,):
            pass
        except Exception as e:
            err_str = "通过选择器：{}，表达式: {}，获取元素失败，error：{}".format(locator, regx, e)
            logger.error(err_str)
        return is_exist

    def get_button(self, locator: str, regx: str) -> WebElement:
        """
        获取按钮
        :return: 按钮对象
        """
        button = None
        try:
            button = self.wait.until(ec.element_to_be_clickable((Locator.get(locator), regx)))
        except Exception as e:
            err_str = "通过选择器：{}，表达式: {}，获取点击按钮失败，error：{}".format(locator, regx, e)
            logger.error(err_str)
        return button

    def get_image_position(self, locator: str, regx: str) -> tuple:
        """
        获取图片位置
        :return: 图片位置元组
        """
        top, bottom, left, right = (-1, -1, -1, -1)
        try:
            img = self.wait.until(ec.presence_of_element_located((Locator.get(locator), regx)))
            location = img.location
            size = img.size
            top, bottom, left, right = location['y'], location['y'] + size['height'], location[
                'x'], location['x'] + size['width']
        except Exception as e:
            err_str = "通过选择器：{}，表达式: {}，获取图片在页面中的位置失败，error：{}".format(locator, regx, e)
            logger.error(err_str)
        return top, bottom, left, right

    def get_screenshot(self) -> tuple:
        """获取当前截屏"""
        screenshot_file_name, screenshot_file_suffix = None, None
        try:
            screenshot_file_suffix = get_current_datetime_int_str()
            screenshot_file_name = os.path.sep.join([self.browser_proxy.IMAGE_PATH, "screenshot_{}.png".format(
                screenshot_file_suffix
            )])
            self.browser.save_screenshot(screenshot_file_name)
        except Exception as e:
            err_str = "获取当前页面截屏失败，error：{}".format(e)
            logger.error(err_str)
        return screenshot_file_name, screenshot_file_suffix

    @classmethod
    def open_image(cls, filename: str) -> bytes:
        image_data = None
        try:
            if is_file(filename) is True:
                # 打开图像文件
                with open(filename, 'rb') as f:
                    image_data = f.read()  # 读取图像文件的二进制数据
            else:
                logger.warning("文件<{}>不存在".format(filename))
        except Exception as e:
            err_str = "打开图片文件<{}>失败， error: {}".format(filename, e)
            logger.error(err_str)
        return image_data

    def get_screenshot_image(self, locator: str, regx: str, image_name: str) -> str:
        """
        从全屏截屏中获取图片
        :return: 图片对象
        """
        file_name = None
        try:
            top, bottom, left, right = self.get_image_position(locator=locator, regx=regx)
            screenshot_file_name, suffix = self.get_screenshot()
            screenshot_img = Image.open(screenshot_file_name)
            # print("图片在屏幕中的位置，左:{}，上:{}，右:{}，下:{}".format(left, top, right, bottom))
            captcha = screenshot_img.crop((left, top, right, bottom))
            file_name = os.path.sep.join([self.browser_proxy.IMAGE_PATH, '{}_{}.png'.format(image_name, suffix)])
            captcha.save(file_name)
        except Exception as e:
            err_str = "通过选择器：{}，表达式: {}，从截屏中获取图片失败， error: {}".format(locator, regx, e)
            logger.error(err_str)
        return file_name

    def move_slider(self, locator: str, regx: str, step: int) -> bool:
        flag = False
        try:
            slider_button = self.get_button(locator=locator, regx=regx)
            action = ActionChains(self.browser)
            action.click_and_hold(slider_button).perform()
            action.move_by_offset(step + 1, 0).perform()
            time.sleep(0.5)
            action.release(on_element=slider_button).perform()  # 松开鼠标左键，完成操作
            time.sleep(2)
            flag = True
        except Exception as e:
            err_str = "通过选择器：{}，表达式: {}，操作鼠标拖动滑块报错，error: {}".format(locator, regx, e)
            logger.error(err_str)
        return flag

    def move_by_offset(self, position_list: list) -> bool:
        flag = False
        try:
            # 创建 ActionChains 对象
            actions = ActionChains(self.browser)
            for x in position_list:
                # 移动鼠标到指定屏幕坐标
                actions.move_by_offset(int(x[0]), int(x[1]))
                # 执行点击操作
                actions.click()
            # 执行所有动作
            actions.perform()
            time.sleep(2)
            flag = True
        except Exception as e:
            err_str = "移动鼠标，依次点击{}屏幕这些位置失败，error: {}".format(position_list, e)
            logger.error(err_str)
        return flag

    @classmethod
    def pending(cls) -> None:
        input("请按回车键退出...\n")

    def get_page_source(self) -> str:
        return self.browser.page_source

    def get_session(self) -> str:
        # 使用 JavaScript 获取网络请求的 Cookie 头部信息
        cookies = self.browser.execute_script("return document.cookie")
        return cookies or ''

    def refresh(self) -> None:
        # 刷新当前页面
        self.browser.refresh()


@element_find_exception
def scroll_to_bottom(driver: webdriver) -> None:
    """模拟页面滚动到底部"""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


@element_find_exception
def get_outer_html(driver: webdriver, element: WebElement) -> str:
    # 使用 JavaScript 获取元素的 outerHTML
    return driver.execute_script("return arguments[0].outerHTML;", element)


@loop_find_element
def get_elements(driver: webdriver, locator: str, regx: str, timeout: int = 3, **kwargs) -> list[WebElement]:
    kwargs.clear()
    return WebDriverWait(driver, timeout).until(
        ec.presence_of_all_elements_located((Locator.get(locator), regx))
    )


@loop_find_element
def get_sub_element(element: WebElement, locator: str, regx: str, **kwargs) -> WebElement:
    kwargs.clear()
    return element.find_element(Locator.get(locator), regx)

import re

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Novel_KDT_TestFrame.keyword.BuildInLibrary import BuildInLibrary
from selenium.webdriver.common.action_chains import ActionChains


class MySeleniumLibrary(BuildInLibrary):
    """类名和模块名是一样的"""

    def open_browser(self, type):
        """打开浏览器"""
        if type in ("chrome", "谷歌"):
            self.dr = webdriver.Chrome()
        elif type in ("firefox", "ff", "火狐"):
            self.dr = webdriver.Firefox()
        else:
            raise TypeError(f"你输入的浏览器类型【 {type} 】不支持！")

    def maximize_browser_window(self):
        """最大化浏览器"""
        self.dr.maximize_window()

    def set_implicitly_wait(self, timeout):
        """设置隐式等待时间"""
        self.dr.implicitly_wait(timeout)

    def go_to(self, url):
        """打开一个网址"""
        self.dr.get(url)

    def my_find_element(self, locator):
        """内置查找元素的方法"""
        by, value = locator.split("=", maxsplit=1)
        return self.dr.find_element(by, value)

    def my_find_elements(self, locator):
        """内置查找元素的方法"""
        by, value = locator.split("=", maxsplit=1)
        return self.dr.find_elements(by, value)

    def input_text(self, locator: str, text, clean=True):
        """输入文本"""
        text = self.replace_parameter(text)  # 替换文本中的参数
        element = self.my_find_element(locator)
        if clean:
            element.clear()  # 清空
        element.send_keys(text)

    def input_password(self, locator, text):
        """输入密码"""
        self.input_text(locator, text)

    def click_element(self, locator, action_chains=False):
        """点击元素"""
        element = self.my_find_element(locator)
        if action_chains is True or (isinstance(action_chains, str) and action_chains.lower() == "true"):
            ActionChains(self.dr).click(element).perform()
        else:
            element.click()

    def element_should_be_visible(self, locator, timeout=5):
        """断言一个元素是可见的"""
        by, value = locator.split("=", maxsplit=1)
        WebDriverWait(self.dr, timeout).until(EC.visibility_of_element_located((by, value)))

    def close_browser(self):
        """关闭浏览器"""
        self.dr.quit()

    def assert_elements_len_should_be(self, loactor, length):
        """断言元素的个数为指定的数量"""
        elements = self.my_find_elements(loactor)
        assert len(elements) == length

    def get_element_text(self, save_param, locator):
        """
        获取一个元素的文本，保存到变量save_param中。
        :param save_param: 保存的变量名
        :param locator: 定位的元素
        :return: None
        """
        element_txt = self.my_find_element(locator).text  # 获取定位元素的文本信息
        save_param_name = re.fullmatch("\{\{(\w+)}}", save_param).group(1)
        self.set_global_parameter(save_param_name, element_txt)  # 保存到变量 glob_parameter


if __name__ == '__main__':
    msl = MySeleniumLibrary()
    msl.open_browser("chrome")
    msl.maximize_browser_window()
    msl.set_implicitly_wait(5)
    msl.go_to("http://1.14.44.5:8080/woniusales")
    msl.input_text("id=username", "admin")
    msl.input_password("id=password", "admin123")
    msl.input_text("id=verifycode", "11xx")
    msl.click_element("class name=form-control.btn-primary")
    msl.element_should_be_visible('link text=注销', 10)
    msl.close_browser()

import re
import time


class BuildInLibrary(object):  # 定义一个可以存储自定义参数的类
    glob_paramter = {}  # 存储参数

    def sleep(self, timeout):
        time.sleep(float(timeout))

    def get_glob_paramter(self, key):
        """获取全局参数"""
        self.glob_paramter["timestr"] = str(int(time.time() * 1000))  # 刷新了时间戳
        self.glob_paramter["unique_no"] = str(int(time.time() * 1000))[-8:]  # 唯一号
        self.glob_paramter["timestr10"] = str(time.time()).split(".")[0]  # 获取当前时间戳前十位整数
        return self.glob_paramter[key]

    def set_global_parameter(self, key, value):
        """保存参数"""
        self.glob_paramter[key] = value

    def replace_parameter(self, text=""):
        """如果text中有 {{参数名}}， 这需要进行替换"""
        # 1.获取所有需要替换的参数名。

        params_list = re.findall("\{\{(\w+)}}", text)
        # 2.替换
        for p in params_list:
            text = text.replace("{{" + p + "}}", self.get_glob_paramter(p))
        # 3.返回
        return text

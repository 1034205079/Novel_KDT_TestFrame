# -*- encoding=utf8 -*-
__author__ = "songxiaofei"  # 作者

from airtest.core.api import *
from airtest.cli.parser import cli_setup
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from Novel_KDT_TestFrame.keyword.BuildInLibrary import BuildInLibrary
from Novel_KDT_TestFrame.config.config import Config


class MyAndroidLibrary(BuildInLibrary):
    """安卓自动化点击操作库"""

    def __init__(self):
        if not cli_setup():
            auto_setup(__file__, logdir=False,  # 不生成log文件
                       devices=[
                           f"android://127.0.0.1:5037/{Config.device_id}?"
                           f"cap_method=ADBCAP&touch_method=MAXTOUCH&"])  # 连接设备
        self.poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)  # 初始化poco

    def open_app(self, package_name: str):
        """启动app"""
        self.package_name = package_name
        start_app(package_name)  # 启动App

    def click_text(self, txt: str):  # 传入元素的文本
        """点击文本"""
        ele = self.poco(text=txt)
        while not ele.exists():
            sleep(1)
        ele.click()

    def click(self, location: str):
        """根据完整路径点击"""
        try:
            ele = self.poco(location)
            ele.wait_for_appearance(timeout=20)
            ele.click()
        except Exception as e:
            raise Exception(f"元素未找到: {e}")

    def swipe(self, direction):  # 传入滑动方向
        """滑动"""
        if direction == "up":  # 向上滑动
            self.poco.swipe([0.5, 0.8], [0.5, 0.2], duration=0.5)
        elif direction == "down":  # 向下滑动
            self.poco.swipe([0.5, 0.2], [0.5, 0.8], duration=0.5)
        elif direction == "left":  # 向左滑动
            self.poco.swipe([0.8, 0.5], [0.2, 0.5], duration=0.5)
        elif direction == "right":  # 向右滑动
            self.poco.swipe([0.2, 0.5], [0.8, 0.5], duration=0.5)
        else:
            raise Exception("请输入up或down")  # 其他方向暂不支持

    def input_text(self, location: str, txt: str):
        """输入文本"""
        try:
            ele = self.poco(location)  # 定位输入框
            ele.wait_for_appearance(timeout=10)  # 等待元素出现
            ele.set_text(txt)  # 输入文本
        except Exception as e:
            raise Exception(f"元素未找到: {e}")

    def clear_cache(self):  # 关闭app,并清空缓存
        clear_app(self.package_name)

    def close_app(self):  # 关闭app
        stop_app(self.package_name)


if __name__ == '__main__':
    mal = MyAndroidLibrary()
    mal.open_app("com.novel.mikan")
    mal.click_text("战焚八荒")
    mal.click_text("Read Now")
    # mal.click("com.novel.mikan:id/wrapper")
    mal.swipe("left")
    # mal.input_text("com.novel.mikan:id/input", "com.novel.mikan:id/input")
    mal.close_app()

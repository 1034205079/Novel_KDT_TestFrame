import time
from Novel_KDT_TestFrame.keyword.BuildInLibrary import BuildInLibrary
from pykeyboard import PyKeyboard
from pymouse import PyMouse

"""封装鼠标键盘的库"""


class MyPyKeyBoardLibrary(BuildInLibrary):
    def __init__(self):
        self.keyboard = PyKeyboard()
        self.pymouse = PyMouse()

    def type_string(self, s):
        """输入内容"""
        self.keyboard.type_string(s)

    def type_hot_key(self, *keys):
        """格式为: enter_key，control_key，alt_key ,escape_key,space_key
        需要把keys = ("alt_key","o")  变换为  [self.keyboard.alt_key,"o"]... ..."""
        keys_list = list(keys)  # 元祖转换成列表
        for index, value in enumerate(keys_list):
            if hasattr(self.keyboard, value):  # 如果self.keyboard有对应的value属性
                keys_list[index] = getattr(self.keyboard, value)  # 就替换为对应的快捷键
        self.keyboard.press_keys(keys_list)

    def click(self, x, y, button=1, n=1):
        """
               Click a mouse button n times on a given x, y.
               Button is defined as 1 = left, 2 = right, 3 = middle.
        """
        self.pymouse.click(x, y, button, n)
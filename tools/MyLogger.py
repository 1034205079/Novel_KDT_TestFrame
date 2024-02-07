import os.path
from Novel_KDT_TestFrame.config.config import Config
import logging


class MyLogger:
    def __init__(self):
        self.logger_name = Config.logger_name
        self.logger_file = os.path.join(Config.project_path, "log/mylog.log")
        self.logger_level = Config.logger_level

    def get_logger(self):
        # 1.获取一个日志记录器
        mylog_recorder = logging.getLogger(self.logger_name)
        # 2.创建文件句柄handler
        filehandler = logging.FileHandler(filename=self.logger_file, mode="w", encoding="utf8")  # 负责把log输出到文件里
        # 3.创建控制台句柄handler
        stream_handler = logging.StreamHandler()  # 负责把log输出到控制台里
        # 4.指定日志的格式format
        display_format = logging.Formatter("%(asctime)s %(levelname)s %(filename)s %(lineno)d --> %(message)s")  # s 可以将输出格式化为字符串
        # 5.设置句柄的格式
        filehandler.setFormatter(display_format)
        stream_handler.setFormatter(display_format)
        # 6.日志记录器绑定句柄
        mylog_recorder.addHandler(filehandler)
        mylog_recorder.addHandler(stream_handler)
        # 7.设置日志记录级别
        mylog_recorder.setLevel(self.logger_level)
        return mylog_recorder


mylogger = MyLogger().get_logger()  # 实例化一个

if __name__ == '__main__':
    mylogger.debug("123123123")

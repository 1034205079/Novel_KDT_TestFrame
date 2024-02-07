import logging

# 1.获取一个日志记录器
mylogger = logging.getLogger("biglogger")
# 2.创建文件句柄handler
filehandler = logging.FileHandler(filename="mylog.log", mode="w", encoding="utf8")
# 3.创建控制台句柄handler
stream_handler = logging.StreamHandler()
# 4.指定日志的格式format
display_format = logging.Formatter("%(asctime)s %(levelname)s %(filename)s %(lineno)d --> %(message)s")
# 5.设置句柄的格式
filehandler.setFormatter(display_format)
stream_handler.setFormatter(display_format)
# 6.日志记录器绑定句柄
mylogger.addHandler(filehandler)
mylogger.addHandler(stream_handler)
# 7.设置日志记录级别
mylogger.setLevel(logging.DEBUG)
# 8.测试日志
mylogger.debug("这是一个debug信息")
mylogger.info("这是一个info信息")
mylogger.warning("这是一个warning信息")
mylogger.error("这是一个error信息")
mylogger.critical("这是一个critical信息")

import logging
import os


class Config:
    project_path = os.path.split(os.path.split(__file__)[0])[0]
    project_name = str(project_path).split('\\')[-1]  # 从路径中拿到项目名
    windows_ip = "172.16.10.34"  # 你电脑的ip地址
    base_url = "http://novel.123.com"  # 你要测试的网站的基础url
    db_info = {"host": "172.16.10.180", "port": 3306, "user": "root", "password": "root", "db": "kdt_test"}  # 数据链接信息，db是数据库名，建议固定
    logger_name = "biglogger"  # 日志名，不重要
    logger_level = logging.DEBUG  # 日志级别
    mail_account = "123@123.com"  # 发送测试报告的邮箱账号
    mail_token = "12345"  # 发送测试报告的邮箱授权码
    mail_smtp = "smtp.qiye.aliyun.com"  # 发送测试报告的邮箱smtp地址
    mail_port = 465  # 发送测试报告的邮箱端口
    receive_mail = ['boss1@123.com', 'boss2@123.com']  # 收件人列表，用列表存储，可以有多个收件人


if __name__ == '__main__':
    print(Config.project_path)
    print(Config.project_name)

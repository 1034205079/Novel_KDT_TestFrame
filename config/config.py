import logging
import os


class Config:
    project_path = os.path.split(os.path.split(__file__)[0])[0]
    project_name = str(project_path).split('\\')[-1]  # 从路径中拿到项目名
    windows_ip = "172.16.10.34"
    base_url = "http://novel.52toolbox.com"
    db_info = {"host": "172.16.10.180", "port": 3306, "user": "root", "password": "root", "db": "kdt_test"}
    logger_name = "biglogger"
    logger_level = logging.DEBUG
    mail_account = "songxiaofei@ludashi.com"
    mail_token = "lq6ugG9jg1z4d4mg"
    mail_smtp = "smtp.qiye.aliyun.com"
    mail_port = 465
    receive_mail = ['songxiaofei@ludashi.com', 'wenrong@ludashi.com',]  # 收件人列表


if __name__ == '__main__':
    print(Config.project_path)
    print(Config.project_name)

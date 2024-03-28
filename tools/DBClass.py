import pymysql
import time
import base64
import re


class DBClass:
    """查询，操作你的数据库"""

    def __init__(self, host, port, user, password, db):
        try:
            self.cnn = pymysql.connect(host=host,
                                       port=port,
                                       user=user,
                                       password=password,
                                       charset="utf8",
                                       db=db,
                                       autocommit=False)  # 关闭自动提交
            self.cur = self.cnn.cursor(pymysql.cursors.DictCursor)  # 以字典的形式查询
        except pymysql.Error as e:
            print(f"Error connecting to the database: {e}")  # 打印异常信息

    def query(self, sql):  # 查询函数
        try:  # 捕获异常
            self.cur.execute(sql)  # 执行sql语句
            result = self.cur.fetchall()  # 获取查询结果
            return result  # 返回查询结果
        except pymysql.Error as e:  # 捕获异常
            print(f"Error executing query: {e}")  # 打印异常信息
            return []  # 返回空列表

    def update(self, *sqls):  # 插入，更新，删除函数
        try:
            for sql in sqls:  # 循环执行sql语句
                self.cur.execute(sql)  # 执行sql语句
            self.cnn.commit()  # 提交事务
        except pymysql.Error as e:  # 捕获异常
            print(f"Error executing update: {e}")  # 打印异常信息
            self.cnn.rollback()  # 回滚事务

    def __del__(self):  # 析构函数，关闭连接
        try:
            self.cur.close()  # 关闭游标
            self.cnn.close()  # 关闭连接
        except AttributeError:
            pass  # 可能在初始化时出现异常，没有创建连接对象

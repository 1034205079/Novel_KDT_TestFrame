import pymysql, time, base64, re


class DBClass(object):
    """查询，操作你的数据库"""

    def __init__(self, host, port, user, password, db):
        self.cnn = pymysql.connect(host=host,
                                   port=port,
                                   user=user,
                                   password=password,
                                   charset="utf8",
                                   db=db,
                                   autocommit=True, )
        self.cur = self.cnn.cursor(pymysql.cursors.DictCursor)  # 以字典的形式查询

    def query(self, sql):
        self.cur.execute(sql)
        result = self.cur.fetchall()
        return result

    def update(self, *sqls):
        self.cnn.begin()
        for sql in sqls:
            self.cur.execute(sql)
        self.cnn.commit()

    def __del__(self):
        self.cur.close()
        self.cnn.close()


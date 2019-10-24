"""
dict 数据端
数据库操作,提供各种服务端需要的数据
"""
import pymysql
import hashlib


def md5_passwd(passwd):
    hash = hashlib.md5()
    hash.update(passwd.encode())
    return hash.hexdigest()


class Database:
    def __init__(self, database,
                 host='localhost',
                 port=3306,
                 user='root',
                 password='123456',
                 charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.connect_db()

    def connect_db(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  password=self.password,
                                  database=self.database,
                                  charset=self.charset)

    def create_cursor(self):
        self.cur = self.db.cursor()

    def register_name(self, username):
        sql = 'select * from user where name = %s'
        self.cur.execute(sql, [username])
        r = self.cur.fetchone()
        if r:
            return True
        else:
            return False

    def register(self, username, passwd):
        password = md5_passwd(passwd)
        sql = 'insert into user (name,passwd) values (%s,%s)'
        try:
            self.cur.execute(sql, [username, password])
            self.db.commit()
        except Exception:
            self.db.rollback()
            return False
        else:
            return True

    def login(self, username, passwd):
        password = md5_passwd(passwd)
        sql = 'select name from user where name=%s and passwd=%s'
        self.cur.execute(sql, [username, password])
        r = self.cur.fetchone()
        if r:
            return True
        else:
            return False

    def close(self):
        if self.cur:
            self.cur.close()
        self.db.close()







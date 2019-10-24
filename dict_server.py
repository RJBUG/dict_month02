"""
dict_server.py 在线词典
服务端
逻辑处理,数据
"""

from socket import *
import sys,os
import signal
from dict_db import Database


ARRD = '127.0.0.1'
PORT = 8888
url = (ARRD, PORT)
db = Database(database='dict')


def do_register_name(c):
    while True:
        username = c.recv(128).decode()
        # 判断用户名是否存在
        if not db.register_name(username):
            c.send(b'OK')
            return username
        else:
            c.send(b'exist')


def do_login(c):
    while True:
        data = c.recv(1024).decode().split(" ")
        username = data[0]
        passwd = data[1]
        if db.login(username, passwd):
            c.send(b'OK')
        else:
            c.send(b'False')


def do_register(c, username):
    passwd = c.recv(128).decode()
    if db.register(username, passwd):
        c.send(b'OK')
        return username
    else:
        c.send(b'False')


def do_query(name, word):
    pass


def request(c):
    db.create_cursor()  # 生成游标
    while True:
        data = c.recv(1024).decode()
        if not data or data == 'Exit':
            c.close()
            return
        elif data == 'Register':
            c.send(b'OK')
            username = do_register_name(c)
            do_register(c, username)
        elif data == 'Login':
            c.send(b'OK')
            do_login(c)
        elif data.split(' ')[0] == 'Q':
            name = data.split(' ')[1]
            word = data.split(' ')[2]
            do_query(name, word)


def main():
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(url)
    sockfd.listen(3)

    # 处理僵尸进程
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    # 循环等待客户端的连接
    print('listen the port 8888.....')
    while True:
        try:
            c, addr = sockfd.accept()
            print('Connect from', addr)
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue

        # 创建子进程
        pid = os.fork()
        if pid == 0:
            sockfd.close()
            request(c)  # 具体处理客户端请求
            os._exit(0)
        else:
            c.close()


if __name__ == '__main__':
    main()




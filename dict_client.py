"""
dict 客户端
发起请求,展示结果
"""

from socket import *
import sys
import getpass
import hashlib


ADDR = '127.0.0.1'
PORT = 8888
URL = (ADDR, PORT)
i = 0
sockfd = socket()
sockfd.connect(URL)


def register():
    while True:
        username = input("请输入用户名:")
        if ' ' in username:
            print('用户名不能有空格!')
        sockfd.send(username.encode())
        data = sockfd.recv(1024).decode()
        if data == 'exist':
            print('用户名存在!')
            continue
        passwd = getpass.getpass('请输入密码:')
        passwd_ = getpass.getpass('请重新输入密码:')
        if passwd != passwd_:
            print('两次密码不相同,请重新输入!')
            continue
        if ' ' in passwd:
            print('密码不能有空格!')
        hash = hashlib.md5()
        hash.update(passwd.encode())
        passwd = hash.hexdigest()
        sockfd.send(passwd.encode())
        data = sockfd.recv(128).decode()
        if data == 'OK':
            print('注册成功')
            return username
        else:
            print('注册失败')
            return False


def login():
    for i in range(5):
        username = input('请输入用户名:')
        passwd = getpass.getpass('请输入用户密码:')
        hash = hashlib.md5()
        hash.update(passwd.encode())
        passwd = hash.hexdigest()
        msg = '%s %s' % (username, passwd)
        sockfd.send(msg.encode())
        data = sockfd.recv(1024).decode()
        if data == 'False':
            print('用户名或密码输入错误!')
            continue
        return username
    else:
        return False


def do_(username):
    while True:
        print("""
    =============welcome============
    1. 查单词  2. 查历史记录    3. 退出
                     """)
        cmd_for_client = input('请输入命令选择功能:')
        if cmd_for_client == '1':
            do_get_word(username)
        elif cmd_for_client == '2':
            do_get_his(username)
        elif cmd_for_client == '3':
            return
        else:
            print('输入错误,请重新输入!')


# 连接服务端
def do_get_word(username):
    while True:
        word = input('word:')
        if word == "":
            break
        msg = 'Q %s %s' % (username, word)
        sockfd.send(msg.encode())
        print(sockfd.recv(2048).decode())


def do_get_his(username):
    msg = 'H %s' % username
    sockfd.send(msg.encode())
    data = sockfd.recv(1024).decode()
    print(data)


def main():


    while True:
        print("""
        ===========welcome============
          1. 注册   2. 登录   3. 退出
        """)
        cmd = input("请选择功能:")
        if cmd == '1':
            sockfd.send(b'Register')
            data = sockfd.recv(1024).decode()
            if data == 'OK':
                name = register()
                if name:
                    do_(name)
        elif cmd == '2':
            sockfd.send(b'Login')
            data = sockfd.recv(1024).decode()
            if data == 'OK':
                name = login()
                if name:
                    do_(name)
        elif cmd == '3':
            sockfd.send(b'Exit')
            sockfd.close()
            sys.exit('谢谢使用')
        else:
            print('请输入正确的命令!')


if __name__ == '__main__':
    main()


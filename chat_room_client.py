# coding:UTF-8
# path:/home/tarena/桌面/study_file/tarena_study/myselfcode/第二阶段/并发编程/May09

"""
作者：朱文涛
邮箱：wtzhu_13@163.com

时间：2019/05
描述：群聊聊天室客户端
功能 ： 类似qq群功能
1. 有人进入聊天室需要输入姓名，姓名不能重复
2. 有人进入聊天室时，其他人会收到通知：xxx 进入了聊天室
3. 一个人发消息，其他人会收到：xxx ： xxxxxxxxxxx
4. 有人退出聊天室，则其他人也会收到通知:xxx退出了聊天室
"""
from socket import *
import os,sys

# 服务器地址
ADDR = ('192.168.0.6', 8888)


# 发送消息
def send_msg(s, name):
    while True:
        try:
            text = input("发言:")
        except KeyboardInterrupt:
            text = 'quit'
        # 退出聊天室
        if text == 'quit':
            msg = "Q " + name
            s.sendto(msg.encode(), ADDR)
            sys.exit("退出聊天室")

        msg = "C %s %s" % (name, text)
        s.sendto(msg.encode(), ADDR)


# 接收消息
def recv_msg(s):
    while True:
        data,addr = s.recvfrom(2048)
        # 服务端发送ＥＸＩＴ表示让客户端退出
        if data.decode() == 'EXIT':
            sys.exit()
        print(data.decode())


# 创建网络链接
def main():
    s = socket(AF_INET,SOCK_DGRAM)
    while True:
        name = input("请输入姓名:")
        msg = "L " + name
        s.sendto(msg.encode(),ADDR)
        # 等待回应
        data, addr = s.recvfrom(1024)
        if data.decode() == 'OK':
            print("您已进入聊天室")
            break
        else:
            print(data.decode())

    # 创建新的进程
    pid = os.fork()
    if pid < 0:
        sys.exit("Error!")
    elif pid == 0:
        send_msg(s, name)
    else:
        recv_msg(s)


if __name__ == "__main__":
    main()

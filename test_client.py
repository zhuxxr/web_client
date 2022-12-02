# -*- coding:utf-8 -*-
"""
作者：苎夏星染
日期：2022年12月01日
"""
import socket
import json


def test_getdata():
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c_socket.connect(("127.0.0.1", 1000))
    temp_list = ["获取信息", "北京"]
    c_socket.send(json.dumps(temp_list).encode("utf-8"))
    accept_data = b''
    while True:
        temp_data = c_socket.recv(1024)
        accept_data += temp_data
        if len(temp_data) < 1024:
            break
    data = json.loads(accept_data.decode("utf-8"))
    c_socket.close()
    assert type(data) == list


def test_save_data():
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c_socket.connect(("127.0.0.1", 1000))
    test_data = [{"城市": "沈阳", "标题": "东北大学 浑南校区", "地址": "浑南区 创新路195号",
                  "详细介绍": "很多室很多厅 | 80000+平方米 | 东 南 西 北 | 精装 | 很多楼 一号楼很高 风很大 | 2016年建成 | 塔楼",
                  "总价": "99999999万", "单价": "9999999万/平", "网址": "https://www.neu.edu.cn/"}]
    temp_list = ["保存信息", test_data]
    c_socket.send(json.dumps(temp_list).encode("utf-8"))
    assert c_socket.recv(1024)
    c_socket.close()


def test_inquire():
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c_socket.connect(("127.0.0.1", 1000))
    temp_list = ["获取图表", 25000]
    c_socket.send(json.dumps(temp_list).encode("utf-8"))
    accept_data = b''
    while True:
        temp_data = c_socket.recv(1024)
        accept_data += temp_data
        if len(temp_data) < 1024:
            break
    data = json.loads(accept_data.decode("utf-8"))
    c_socket.close()
    assert type(data) == dict


def test_other():
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c_socket.connect(("127.0.0.1", 1000))
    send = "我也不知道我送过去了啥，反正我是送过去了"
    c_socket.send(json.dumps(send).encode("utf-8"))
    accept_data = b''
    while True:
        temp_data = c_socket.recv(1024)
        accept_data += temp_data
        if len(temp_data) < 1024:
            break
    data = json.loads(accept_data.decode("utf-8"))
    c_socket.close()
    assert data

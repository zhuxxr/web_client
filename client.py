# -*- coding:utf-8 -*-
"""
作者：苎夏星染
日期：2022年11月30日
"""
import socket
import tkinter.ttk
import tkinter as tk
import re
import pandas as pd
import matplotlib.pyplot as plt
from cityfile import *
import json


def getdata():
    table.delete(*table.get_children())
    temp = Cities()
    if not re.match(r'^[a-z]+[a-z]$', "".join(pypinyin.lazy_pinyin(a.get(), style=pypinyin.Style.FIRST_LETTER))):
        logger.warning("Information-compliant characters were entered")
        entry1.delete(0, "end")
        root.update()
        return
    elif a.get() not in temp.dict_city.keys():
        logger.warning("The City name does not exist in the file")
        entry1.delete(0, "end")
        root.update()
        return
    client_list = ["获取信息", a.get()[:]]
    client_socket.send(json.dumps(client_list).encode("utf-8"))
    accept_data = b''
    while True:
        temp_data = client_socket.recv(1024)
        accept_data += temp_data
        if len(temp_data) < 1024:
            break
    infos = json.loads(accept_data.decode("utf-8"))[:]
    global city
    n = 0
    for info in infos:
        n += 1
        table.insert("", "end", values=(
            str(n), info["标题"], info["地址"], info["详细介绍"], info["总价"], info["单价"], info["网址"]))
        info["城市"] = a.get()
    city = infos[:]
    root.update()
    logger.info("Second-hand housing information query success")
    entry1.delete(0, "end")


def save_data():
    global datas
    datas = datas + city[:]
    if len(datas) == 0:
        logger.warning("Storage information does not exist")
        return
    client_list = ["保存信息", datas[:]]
    client_socket.send(json.dumps(client_list).encode("utf-8"))
    if not client_socket.recv(1024):
        return
    pf = pd.DataFrame(datas)
    order = ["城市", "标题", "地址", "详细介绍", "总价", "单价", "网址"]
    pf = pf[order]
    file_path = pd.ExcelWriter("ershoufang.xlsx", mode='w', engine="openpyxl")
    pf.to_excel(file_path, index=False)
    logger.info("Information storage was successful")
    file_path.close()


def inquire_chart():
    if new_var.get() == "":
        return
    elif not re.match(r"^[0-9]+[0-9]$", new_var.get()):
        entry.delete(0, "end")
        return
    root.withdraw()
    inquire_list = ["获取图表", int(new_var.get()[:])]
    client_socket.send(json.dumps(inquire_list).encode("utf-8"))
    accept_data = b''
    while True:
        temp_data = client_socket.recv(1024)
        accept_data += temp_data
        if len(temp_data) < 1024:
            break
    data = json.loads(accept_data.decode("utf-8"))
    plt.rcParams["font.sans-serif"] = ['SimHei']
    plt.rcParams["axes.unicode_minus"] = False

    plt.figure(figsize=(4.8, 3), dpi=150)
    for key in data.keys():
        bar = plt.bar(key, data[key])
        plt.bar_label(bar, label_type="edge", size=6)
    plt.xticks(rotation=60, size=6)
    plt.yticks(size=6)
    plt.title("城市二手房数量", fontdict={'size': 8})
    plt.ylabel("二手房数量", fontdict={'size': 8})
    plt.tight_layout()
    plt.savefig("cities.png")

    new_root = tk.Toplevel()
    new_root.overrideredirect(True)
    new_screenwidth = new_root.winfo_screenwidth()
    new_screenheight = new_root.winfo_screenheight()
    new_width = 900
    new_height = 500
    new_size = f"{new_width}x{new_height}+{int((new_screenwidth - new_width) / 2)}+{int((new_screenheight - new_height) / 2)}"
    new_root.geometry(new_size)
    new_root.resizable(False, False)
    new_root["bg"] = "white"
    img = tk.PhotoImage(file="cities.png")
    image = tk.Label(new_root, image=img)
    image.pack()
    btu2 = tkinter.ttk.Button(new_root, text="关闭", command=lambda: close_win(new_root))
    btu2.pack(pady=5)
    entry.delete(0, "end")
    new_root.mainloop()


def close_win(root_):
    root_.destroy()
    root.deiconify()


if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 1000))

    city, datas = [], []
    root = tk.Tk()
    root.title("二手房信息")
    width = 1500
    height = 800
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = f"{width}x{height}+{int((screenwidth - width) / 2)}+{int((screenheight - height) / 2)}"
    root.geometry(size)
    root.resizable(False, False)
    root["bg"] = "MintCream"
    text1 = tk.Label(root, text="二手房信息", bg='Honeydew', fg="#008080", font=('华文楷体', 20))
    text1.pack()
    frame = tk.Frame(root)
    text2 = tk.Label(frame, text="请输入城市:", bg="MintCream", font="楷体")
    text2.pack(side="left")
    a = tk.StringVar()
    entry1 = tkinter.ttk.Entry(frame, textvariable=a)
    entry1.pack(side="left")
    frame.pack(pady=5)
    button1 = tkinter.ttk.Button(root, text="查询", command=getdata)
    button1.pack()
    button2 = tkinter.ttk.Button(root, text="保存", command=save_data)
    columns = ['序号', '标题', '地址', '详细介绍', '总价', '单价', '网址']
    y_scroll = tk.Scrollbar(root, orient=tk.VERTICAL)
    table = tkinter.ttk.Treeview(root, columns=columns, show='headings', yscrollcommand=y_scroll)
    table.column("序号", width=5)
    table.column("标题", width=250)
    table.column("地址", width=100)
    table.column("详细介绍", width=300)
    table.column("总价", width=20)
    table.column("单价", width=25)
    table.column("网址", width=255)
    table.heading("序号", text="序号")
    table.heading("标题", text="标题")
    table.heading("地址", text="地址")
    table.heading("详细介绍", text="详细介绍")
    table.heading("总价", text="总价")
    table.heading("单价", text="单价")
    table.heading("网址", text="网址")
    y_scroll.config(command=table.yview)
    y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    table.pack(fill=tk.BOTH, expand=True, padx=20, pady=20, ipadx=5, ipady=3)
    text3 = tk.Label(root, text="获取低于目标价格的城市二手房信息", bg="white", font="楷体")
    text3.pack(pady=(0, 5))
    new_frame = tk.Frame(root)
    new_text = tk.Label(new_frame, text="请输入单价:", bg="white", font="楷体")
    new_var = tk.StringVar()
    entry = tkinter.ttk.Entry(new_frame, textvariable=new_var)
    button3 = tkinter.ttk.Button(new_frame, text="获取图表", command=inquire_chart)
    new_text.pack(side="left")
    entry.pack(side="left")
    button3.pack(side="left")
    new_frame.pack(pady=(0, 5))
    button2.pack(pady=(0, 20))
    root.mainloop()
    client_socket.close()

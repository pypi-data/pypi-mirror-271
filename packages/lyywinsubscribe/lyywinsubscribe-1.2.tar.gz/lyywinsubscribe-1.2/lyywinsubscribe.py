import os
import sys
import time
import tkinter as tk
import threading
from datetime import datetime, date
import f1999cfg
from tkinter import scrolledtext
import pandas as pd
# import lyycfg
#
import lyyprocess
icolist = ["--", "\\", "|", "/"]


class gui_subscribe_class:
    def __init__(self, main_module) -> None:
        self.main_module = main_module
        self.gui_reason_module = None
        self.win_subcribe = tk.Toplevel(self.main_module.root)
        self.main_module.win_sub_dict[len(self.main_module.win_sub_dict)] = self.win_subcribe
        # self.gui_reason_module.update_win(self.win_subcribe)
        窗口win启动 = True
        self.win_subcribe.title = "信息监控"
        # self.win_subcribe.protocol('WM_DELETE_WINDOW', self.隐藏到任务栏)  # 把点击x关闭窗口变成不要关闭并最小化到托盘
        # 设置大小 居中展示
        # win.bind("<Configure>", lambda root:win_mouse_release(root))
        self.win_subcribe.resizable(width=False, height=False)
        self.win_subcribe.wm_attributes("-topmost", 1)
        self.win_subcribe.iconbitmap("icon\\Crab.ico")
        self.win_subcribe.geometry("350x670")
        width = 350
        height = 500
        self.win_subcribe.geometry("350x670" + "+" + str(self.main_module.root.winfo_x() + self.main_module.root.winfo_width()) + "+" + str(self.main_module.root.winfo_y()))
        # 注册关闭事件处理函数
        self.win_subcribe.protocol("WM_DELETE_WINDOW", lambda:self.main_module.gui_function.on_close(self.win_subcribe))

        # 注册最小化事件处理函数
        self.win_subcribe.protocol("WM_ICONIFY", lambda:self.main_module.gui_function.on_minimize(self.win_subcribe))

        # 注册恢复事件处理函数
        self.win_subcribe.protocol("WM_DEICONIFY", lambda:self.main_module.gui_function.on_restore(self.win_subcribe))
        # a,b=400,650
        # c=(win.winfo_screenwidth()-a)/2
        # d=(win.winfo_screenheight()-b)/2
        # win.geometry('%dx%d+%d+%d' % (a,b,c,d))
        # win.minsize(400,150)
        self.create_widgets()   
        
        
        


        
    def create_widgets(self):
        lb1 = tk.Label(self.win_subcribe, text="输入关键字")
        lb1.place(relx=0.01, rely=0.02, relwidth=0.24, relheight=0.06)
        lb1["fg"] = "yellow"
        lb1["bg"] = "green"
        lb_结果数量 = tk.Label(self.win_subcribe, text="结果数：")
        lb_结果数量.place(relx=0.6, rely=0.02, relwidth=0.19, relheight=0.06)
        self.设置_查询结果数 = tk.StringVar()
        text_结果数量 = tk.Entry(self.win_subcribe, width=4, textvariable=self.设置_查询结果数)
        text_结果数量.place(relx=0.76, rely=0.02, relwidth=0.08, relheight=0.06)
        text_结果数量.insert(1, "40")

        global label_lastresult
        label_lastresult = tk.StringVar()
        lb2 = tk.Label(self.win_subcribe, text="", textvariable=label_lastresult)
        lb2.place(relx=0.9, rely=0.02)
        label_lastresult.set("0")

        global keyword1, keyword2, keyword3, keyword4, keyword5
        self.keyword1 = tk.Entry(self.win_subcribe, width=7)
        self.keyword1.place(relx=0.02, rely=0.09, relwidth=340, relheight=0.06)

        # keyword1.pack()
        self.keyword2 = tk.Entry(self.win_subcribe, width=7)
        self.keyword2.place(relx=0.22, rely=0.09, relwidth=0.15, relheight=0.06)
        # keyword2.pack()
        self.keyword3 = tk.Entry(self.win_subcribe, width=7)
        self.keyword3.place(relx=0.42, rely=0.09, relwidth=0.15, relheight=0.06)
        # keyword3.pack()
        self.keyword4 = tk.Entry(self.win_subcribe, width=7)
        self.keyword4.place(relx=0.62, rely=0.09, relwidth=0.15, relheight=0.06)

        self.keyword5 = tk.Entry(self.win_subcribe, width=7)
        self.keyword5.place(relx=0.82, rely=0.09, relwidth=0.15, relheight=0.06)
        # keyword4.pack()

        bt1 = tk.Button(self.win_subcribe, text="查 询", command=lambda: self.线程订阅关键字("查询"))
        bt1.place(relx=0.28, rely=0.018, relwidth=0.12, relheight=0.06)
        bt2 = tk.Button(self.win_subcribe, text="订 阅", command=lambda: self.线程订阅关键字("订阅"))
        bt2.place(relx=0.43, rely=0.018, relwidth=0.12, relheight=0.06)

        self.关键字结果文本框 = scrolledtext.ScrolledText(self.win_subcribe)
        self.关键字结果文本框.place(relx=0.01, rely=0.18, relwidth=0.99, relheight=0.75)
        # plantxt.pack()
        # keyword1.bind("<Double-Button>", lambda:keyword1.select_adjust("end"))
        # self.keyword1.bind_class("Entry", "<Button-3>", self.show_right_mouse_menu)
        self.状态栏文本变量win1 = tk.StringVar()
        statusbarwin1 = tk.Label(self.win_subcribe, text="", textvariable=self.状态栏文本变量win1, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        statusbarwin1.place(relx=0.01, rely=0.92, relwidth=340, relheight=0.08)
        self.状态栏文本变量win1.set("状态栏文本变量win1")
        # self.keyword1.bind_class("Entry","<Button-3>",self.bind_righ_menu_entry)
        # 定义一个全局变量，记录窗口是否全屏
        self.menubar = tk.Menu(self.win_subcribe, tearoff=False)

    def win_sub(self):
        # 文本框_主消息.bind('<Button-3>', lambda x: rightKey(x, 文本框_主消息))
        self.win_subcribe.mainloop()

    def 订阅关键字(self, command):
        print("订阅关键字")
        self.订阅关键字fun(command, f1999cfg.info_cfg.subscribe_teachers)

    def 线程订阅关键字(self, command):
        线程参数 = True
        thistime = datetime.now().strftime("%H:%M:%S")

        self.状态栏文本变量1.set(thistime + " run_threaded:" + self.订阅关键字.__name__)
        # print("准备启动线程："+getattr(job_func,'__name__'))
        if lyyprocess.重复线程检测(self.订阅关键字):
            print("线程已经启动，直接返回")
            return
        else:
            job_thread = threading.Thread(name=self.订阅关键字.__name__, target=self.订阅关键字, kwargs={"command": command}, daemon=True)
            job_thread.start()

    def 拼合关键字(self):
        arr = [self.keyword1.get(), self.keyword2.get(), self.keyword3.get(), self.keyword4.get(), self.keyword5.get()]
        text = ""
        fulltext = ""
        print(arr)
        for item in arr:
            if len(item) > 0:
                text = "or message like '%" + item + "%' "
                fulltext = fulltext + text
        fulltext = fulltext.replace("or", "where (", 1)
        print("fulltext=" + fulltext)
        return fulltext

    def 订阅关键字fun(self, command, 额外信息):
        print("订阅关键字")
        text = ""
        global 最后查询结果df, label_lastresult, 设置_查询结果数, 关键字结果文本框
        global 订阅关键字lastid
        engine = f1999cfg.get_engine()
        while True:
            if "查询" in command:
                订阅关键字lastid = 0
            else:
                订阅关键字lastid = label_lastresult.get()
            start = "select id,replace(date_format(time, '%m-%d %H:%i'),concat(CURDATE(),' '),'') as shorttime,chinesename,message from stock_info "
            keywordlist = self.拼合关键字()
            end = f") and id> {订阅关键字lastid} order by time desc limit {self.设置_查询结果数.get()}"
            sqlquery = start + keywordlist + end

            data, df = self.queryMySQL(engine, sqlquery, 订阅关键字lastid)
            # print("df",df)
            self.状态栏文本变量win1.set("最后查询：" + str(datetime.now())[11:19])

            if not df.empty:
                label_lastresult.set(df.loc[0:0]["id"].values.tolist()[0])
                rpltxt = str(date.today())[5:10] + " "
                # print("rpltxt="+rpltxt)
                for row in reversed(data):
                    current = row[1].replace(rpltxt, "") + " " + row[2].replace("vip", "").replace("理解", "").replace("游资", "").replace("投研", "") + ":" + row[3]
                    text = text + current
                    try:
                        # print(win)
                        if isinstance(self.win_subcribe, tk.Toplevel) and self.win_subcribe.state() not in ["iconic", "withdrawn"]:
                            print("win还在,插入win")
                            self.关键字结果文本框.insert("1.0", current + "\n\n")
                            self.关键字结果文本框.insert("1.0", "----------------------------" + "\n")
                            self.关键字结果文本框.see()
                        else:
                            # print(win.state())
                            print("win不在，插入root")
                            self.文本框_主消息.insert("1.0", current + "\n\n")
                            self.文本框_主消息.insert("1.0", "----------------------------" + "\n")
                    except Exception as e:
                        print(e)

                # lyySpeaker(text[12:40])
            time.sleep(1)
            最后查询结果df = df
            global 关键字查询次数
            self.状态栏文本变量3.set(icolist[关键字查询次数 % 4])
            关键字查询次数 += 1

            if "查询" in command:
                订阅关键字lastid = 0
                break

    def queryMySQL(self, conn, sql, lastid):
        sql = sql.replace("mylastid", str(lastid))
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        columnDes = cur.description  # 获取连接对象的描述信息
        if not cur.description:
            columnNames = []
        else:
            columnNames = [columnDes[i][0] for i in range(len(columnDes))]  # 获取列名
        df = pd.DataFrame(data, columns=columnNames)  # 将数据存入 DataFrame 中
        return data, df

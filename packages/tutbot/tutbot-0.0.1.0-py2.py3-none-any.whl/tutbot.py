# 1.0.2

import json, threading
import websocket
import threading
import json
import time
import requests

class Events:
    def __init__(self, url):
        self.url = url
        self.ws = None

    def connect(self):
        self.ws = websocket.WebSocketApp(self.url,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        threading.Thread(target=self.ws.run_forever).start()
        threading.Thread(target=self.heart).start()

    def heart(self):
        while True:
            time.sleep(10)
            self.ws.send("2")

    def on_open(self, ws):
        print("Events : 连接成功")

    def on_message(self, ws, message):
        threading.Thread(target=self.hasmsg, args=(message,)).start()

    def on_error(self, ws, error):
        print("Events : 出现错误 - " + str(error))

    def on_close(self, ws):
        print("Events : 连接断开")

    def send_message(self, message):
        if self.ws:
            self.ws.send(message)
    
    def hasmsg(self,msg):
        print(msg)

class Report:
    def __init__(self,server,port):
        self.post_url = f"http://{server}:{port}/"
        
    def sendpm(self,bot,qq,msg):
        url = self.post_url + "send_msg"
        data = {
            "bot": bot,
            "qq": qq,
            "msg": msg,
            "type": 1
        }

        response = requests.post(url, data=data)

        if response.status_code != 200:
            return False
        return True
    
    def sendgm(self,bot,gid,msg):
        url = self.post_url + "send_msg"
        data = {
            "bot": bot,
            "group": gid,
            "msg": msg,
            "type": 2
        }

        response = requests.post(url, data=data)

        if response.status_code != 200:
            return False
        return True
    
    
    def sendgv(self,bot,gid,url):
        url = self.post_url + "upload_group_pic"
        data = {
            "bot": bot,
            "group": gid,
            "pic": url
        }

        code = requests.post(url, data=data).json()['data']
        print(code)
        return self.sendgm(bot,gid,code)
    
    
    def get_nick(self,bot,qq):
        url = self.post_url + "get_nick"
        data = {
            "bot": bot,
            "qq": qq
        }

        code = requests.post(url, data=data).json()['data']
        return code

class Bot():
    def __init__(self,qq,hasgm=None,haspm=None):
        print('机器人，启动！')
        self.qq = qq
        self.server = '127.0.0.1'
        self.events_port = 5001
        self.report_port = 5000
        self.events = Events(f'ws://{self.server}:{self.events_port}/')
        self.report = Report(self.server,self.report_port)

        if hasgm:
            self.hasgm = hasgm
        if haspm:
            self.haspm = haspm
        
        self.events.hasmsg = self.hasmsg
        self.events.connect()


    def hasmsg(self,msg):
        text = json.loads(msg) 

        if text["bot"] != self.qq:
            return
        
        if text["event"] == "GroupMsg":
            rep = self.hasgm(text["group"],text["qq"],text["msg"])
            if rep != None:
                self.report.sendgm(self.qq,text["group"],rep)

        if text["event"] == "PrivateMsg":
            rep = self.haspm(text["qq"],text["msg"])
            if rep != None:
                self.report.sendpm(self.qq,text["qq"],rep)

    def hasgm(self,gid,uid,text):
        print(text)
        if gid == 771722957:
            return '群消息测试'
        
    def haspm(self,uid,text):
        print(text)
        return '私聊消息测试'
    
    def sendpm(self,qq,text):
        return self.report.sendpm(self.qq,qq,text)

    def sendgm(self,gid,text):
        return self.report.sendgm(self.qq,gid,text)
    
    def sendgv(self,gid,text):
        return self.report.sendgv(self.qq,gid,text)
    
    def get_nick(self,qq):
        return self.report.get_nick(self.qq,qq)


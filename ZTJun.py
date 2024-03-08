#ZTJun.py 不能直接使用，还需要Cookie.yml文件，并在其中增加如下配置填好
#Ztjun:
#    send: 1
#    cookies:
#        - user:
#            name: ""
#            username: ""
#            password: ""
#            cookie: ""
#            user_agent: ""
#参考自：https://github.com/KD-happy/KDCheckin

#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
cron: 0 6 * * *
new Env('ztjun博客签到');
"""
import os
import time
import requests, re, sys, traceback
from io import StringIO
from KDconfig import getYmlConfig, send
import requests
from bs4 import BeautifulSoup


class Ztjun:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.username = ''
        self.password = ''
        self.session = requests.session()
        self.session.headers = {
            "authority": "ztjun.fun",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://ztjun.fun",
            "referer": "https://ztjun.fun",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69",
            "x-requested-with": "XMLHttpRequest"
        }

    def get_login_nonce(self):
        url = 'https://ztjun.fun/login'
        response = self.session.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', {'id': 'main-js-extra'})
        if script_tag:
            script_text = script_tag.string
            match = re.search(r'"ajax_nonce":"(.*?)",', script_text)
            ajax_nonce = match.group(1)
        nonce = ajax_nonce
        print(f'{self.username}的login_nonce为:{nonce}')
        return nonce

    def login(self, username='', password=''):
        nonce = self.get_login_nonce()
        url = "https://ztjun.fun/wp-admin/admin-ajax.php"
        payload = {
            'action': 'zb_user_login',
            'user_name': username or self.username,
            'user_password': password or self.password,
            'remember': '1',
            'nonce': nonce
        }

        response = self.session.post(url, data=payload)
        response.encoding = 'utf-8'
        print(f'{self.username}:\t{response.json()}')
        return self.session

    def get_nonce(self):
        url = 'https://ztjun.fun/user/coin'
        response = self.session.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', {'id': 'main-js-extra'})
        if script_tag:
            script_text = script_tag.string
            match = re.search(r'"ajax_nonce":"(.*?)",', script_text)
            ajax_nonce = match.group(1)
        nonce = ajax_nonce
        print(f'{self.username}的nonce为:{nonce}')
        return nonce

    def sign(self):
        self.login()
        nonce = self.get_nonce()
        url = "https://ztjun.fun/wp-admin/admin-ajax.php"
        # payload = f"action=user_qiandao&nonce={nonce}"
        payload = {
            'action': 'zb_user_qiandao',
            'nonce': nonce
        }
        response = self.session.post(url, data=payload)
        response.encoding = 'utf-8'
        data = response.json()
        print(data)
        if '签到成功' in data.get('msg'):
            self.sio.write(f'签到成功，奖励已到账：0.3积分\n')
            print(f'签到成功，奖励已到账：0.3积分')
        else:
            if '今日已签到' in data.get('msg'):
                self.sio.write('今日已签到\n')
                print('今日已签到')
            else:
                self.sio.write('账号密码错误或Cookie失效\n')
                print('账号密码错误或Cookie失效')

    def SignIn(self):
        print("【治廷君博客签到 日志】")
        self.sio.write("【治廷君博客】\n")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            print(f"{cookie.get('name')} 开始签到...")
            self.sio.write(f"{cookie.get('name')}: ")
            self.username = cookie.get('username')
            self.password = cookie.get('password')
            self.cookie = cookie.get('cookie')
            self.user_agent = cookie.get('user_agent')
            try:
                self.sign()
            except:
                print(f"{cookie.get('name')}: 异常 {traceback.format_exc()}")
                if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                    self.sio.write('签到存在异常, 请自行查看签到日志\n')
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('Ztjun')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            ztjun = Ztjun(Cookies['cookies'])
            sio = ztjun.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('ztjun', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 ztjun 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 ztjun')

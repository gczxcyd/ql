#cutecloud_checkin.py 不能直接使用，需要配置环境变量 cutecloud_email 和 cutecloud_password

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# [task_local]
# cutecloud签到
# 0 */2 * * * cutecloud_checkin.py, tag=cutecloud签到, enabled=true

import requests
import os

session = requests.session()

# 登录
def login(username, password):
    url = "https://www.cute-cloud.top/auth/login"

    headers = {
        "authority": "www.cute-cloud.top",
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
    }

    response = session.post(url, data={
        "email": username,
        "passwd": password
    }, headers=headers)
    print(response.json())

def check_in():
    url = "https://www.cute-cloud.top/user/checkin"
    response = session.post(url)
    print(response.json())

def main():
    username = os.getenv("cutecloud_email")
    password = os.getenv("cutecloud_password")
    login(username, password)
    check_in()

if __name__ == '__main__':
    main()

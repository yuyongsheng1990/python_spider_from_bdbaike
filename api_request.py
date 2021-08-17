# -*- coding: UTF-8 -*-
# @Project -> File: python_spider_from_bdbaike -> spider_baike_text_picture
# @Time: 2021/6/3 20:13
# @Author: Yu Yongsheng
# @Description: 模拟的api调用程序，记得先启动服务器

import requests
def request_data(url):
    req = requests.get(url, timeout=30)  # 请求连接
    req_json = req.content.decode('utf-8')  # 获取数据
    print(req_json)

# 在调用api接口之前，先启动服务器，否则Failed to establish a new connection
if __name__ == '__main__':
    name = '潘建伟'
    url = 'http://192.168.0.101:8891/' + name
    request_data(url)
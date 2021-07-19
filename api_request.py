
# -*- coding: UTF-8 -*-
# @Project -> File: python_spider_from_bdbaike -> spider_baike_text_picture
# @Time: 2021/6/3 20:13
# @Author: Yu Yongsheng
# @Description: 从百度百科爬取人物的基本信息、信息框数据和图片

import requests
def request_data(url):
    req = requests.get(url, timeout=30)  # 请求连接
    req_json = req.json()  # 获取数据
    print(req_json)

if __name__ == '__main__':
    url = 'http://127.0.0.1:5000/潘建伟'
    request_data(url)
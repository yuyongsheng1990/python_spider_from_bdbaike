# -*- coding: UTF-8 -*-
# @Project -> File: python_spider_from_bdbaike -> spider_baike_text_picture
# @Time: 2021/6/3 20:13
# @Author: Yu Yongsheng
# @Description: 利用flask创建API查询接口

import json
import re

import spider_claw
import spider_downloader

import urllib
from bs4 import BeautifulSoup

# 安装Restful package
from flask import Flask, request, jsonify
from flask_restful import reqparse, abort, Api, Resource


# 防止ssl报错
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 初始化app, api
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 接受测试程序发送的调用api的查询请求url，并将查询请求url最后"/"后面的查询字符串(人名)输入到主函数home(name)中
@app.route('/<name>')
def home(name):

    # 去除favicon.ico干扰
    if name =="favicon.ico":
        pass
    else:
        # 判断百度百科上是否存在这个人的页面，或该人名页面是否需要人工跳转
        # 访问、下载html网页
        url = 'https://baike.baidu.com/item/' + urllib.parse.quote(name)  # 请求地址
        # 请求头部，伪造浏览器，防止爬虫被反
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        # 利用请求地址和请求头部构造请求对象
        req = urllib.request.Request(url=url, headers=headers, method='GET')
        response = urllib.request.urlopen(req)  # 发送请求，获得响应
        text = response.read().decode('utf-8')  # 读取响应，获得文本
        # 解析html网页
        soup = BeautifulSoup(text, 'html.parser')  # 创建soup对象，获取html源码
        # 检查该人名的百科页面是否存在sorryCont标签，来判断该页面是否存在
        if soup.find('p', class_='sorryCont'):
            return "查询人物页面不存在，请检查人名输入是否正确"
        # 检查重名人物的百科页面是否需要人工跳转
        href = ""
        if not (soup.find('div', class_=re.compile("para-title level-2")) or soup.find('div', class_=re.compile("lemma-summary"))):
            tag_manual = soup.find('ul', class_=re.compile('custom_dot')).find('li', class_=re.compile('list-dot'))
            href_tag = tag_manual.select('a[target="_blank"]')
            href = href_tag[0].get('href')

        intro, profile_dict, br_text_list, img_list = spider_claw.claw(name, href)
        intro_dict, profile_dict, cv_output = spider_downloader.download(name, intro, profile_dict, br_text_list, img_list)
        output = [intro_dict, profile_dict, cv_output]
        # print(output)
        output_json = json.dumps(output, indent=4, ensure_ascii=False)
        return output_json


if __name__ == '__main__':
    # 设置ip、端口
    app.run(host='192.168.0.101', port=8891)
    # 启动api接口
    # app.run()

    # 调试程序
    # trigger = True
    # while (trigger):
    #     name = '赵忠尧'  # input('查询词语：')
    #     value = home(name)
    #     # intro, profile_dict, br_text_list, img_list = spider_claw.claw(name)
    #     # intro_dict, profile_dict, cv_output = spider_downloader.download(name, intro, profile_dict, br_text_list, img_list)
    #     # output = [intro_dict, profile_dict, cv_output]
    #     print(value)
    #     # print("查询结果：%s" % result)
    #     trigger = False


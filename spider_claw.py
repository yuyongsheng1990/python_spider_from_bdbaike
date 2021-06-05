# -*- coding: UTF-8 -*-
# @Project -> File: python_spider_from_bdbaike -> spider_main
# @Time: 2021/6/8 15:24 
# @Author: Yu Yongsheng
# @Description: 根据提供的人名，爬取其在百度百科的基本信息、信息框、图片。2021.6.7，韩老师要求继续爬取人物履历信息，包括：担任职务、人物经历、
# 人物荣誉、主要著作、参考文献等，我决定将其功能加在基本信息文件中。

import urllib
from bs4 import BeautifulSoup
import re
import requests

# 爬虫程序
def claw(content):
    # 访问、下载html网页
    url = 'https://baike.baidu.com/item/' + urllib.parse.quote(content)      # 请求地址
    # 请求头部，伪造浏览器，防止爬虫被反
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    # 利用请求地址和请求头部构造请求对象
    req = urllib.request.Request(url=url, headers=headers, method='GET')
    response = urllib.request.urlopen(req)      # 发送请求，获得响应
    text = response.read().decode('utf-8')      # 读取响应，获得文本
    # ----------------------------------------------------------------------------------------------------
    # 解析html网页
    soup = BeautifulSoup(text, 'lxml')  # 创建soup对象，获取html源码

    intro_tag = soup.find_all('div', class_="lemma-summary")  # 获取百科基本信息列表
    name_tag = soup.find_all('dt', class_="basicInfo-item name")  # 找到所有dt标签，返回一个标签列表
    value_tag = soup.find_all('dd', class_="basicInfo-item value")  # 找到所有dd标签，返回一个标签列表

    # 处理基本信息：过滤数据，去掉空白
    intro_after_filter = [re.sub('\n+', '', item.get_text()) for item in intro_tag]
    intro_after_filter = [''.join(i.split()) for i in intro_after_filter]  # 去除/0a乱码
    # 将字符串列表连成字符串并返回
    intro_after_filter = ''.join(intro_after_filter)
    # print(intro_after_filter)

    # 抽取信息框数据
    profile_info = {}
    namelist = []
    valuelist = []

    for i in name_tag:  # 将所有dt标签内容存入列表
        name = i.get_text()
        name = ''.join(name.split())  # 去除/0a乱码
        namelist.append(name)
    for i in value_tag:  # 将所有dd标签内容存入列表
        value = i.get_text().strip(' ')
        # value = re.sub('\n+', '、', i.get_text()).strip('、')  # 老师不让删除换行符
        # value = ''.join(value.split())  # 删除可能存在的乱吗/0a，但一块把空格删除了，实际上不需要
        valuelist.append(value)
    for i, j in zip(namelist,
                    valuelist):  # 多遍历循环，zip()接受一系列可迭代对象作为参数，将对象中对应的元素打包成一个个tuple（元组），然后返回由这些tuples组成的list（列表）。
        profile_info[i] = j
    # print(profile_info)

    # 爬取图片
    # 找到所有img标签，返回一个url的标签列表
    img_urllist = []
    resp = requests.get(url=url, headers=headers)
    content = resp.content
    soup = BeautifulSoup(content, 'lxml')
    # img_list = soup.select('div .album-wrap')
    img_list = soup.select('a>div>img')
    # print(img_list)
    for img in img_list:
        try:
            # src = img.find('img').get('src')
            src = img.get('src')
            if re.match(r'https:(.*)image(.*)auto$', src):
                img_urllist.append(src)
        except:
            continue

    # print(img_urllist)
    return intro_after_filter, profile_info, img_urllist
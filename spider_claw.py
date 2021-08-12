# -*- coding: UTF-8 -*-
# @Project -> File: python_spider_from_bdbaike -> spider_main
# @Time: 2021/6/8 15:24 
# @Author: Yu Yongsheng
# @Description: 根据提供的人名，爬取其在百度百科的基本信息、信息框、图片。2021.6.7，韩老师要求继续爬取人物履历信息，包括：担任职务、人物经历、
# 人物荣誉、主要著作、参考文献等，我决定将其功能加在基本信息文件中。
import pickle
import sys
import urllib
from cProfile import label

import bs4
import urllib3.util
from bs4 import BeautifulSoup
import re
import requests

# 爬虫程序
def claw(content, href=''):
    # 访问、下载html网页
    if href:
        url = 'https://baike.baidu.com' + href
    else:
        url = 'https://baike.baidu.com/item/' + urllib.parse.quote(content)  # 请求地址
    # 请求头部，伪造浏览器，防止爬虫被反
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    # 利用请求地址和请求头部构造请求对象
    req = urllib.request.Request(url=url, headers=headers, method='GET')
    response = urllib.request.urlopen(req)  # 发送请求，获得响应
    text = response.read().decode('utf-8')  # 读取响应，获得文本
    # ----------------------------------------------------------------------------------------------------
    # 解析html网页
    soup = BeautifulSoup(text, 'html.parser')  # 创建soup对象，获取html源码
    # 删除人物履历中的description内容标签，因为它的文本是噪音数据，有span和div标签
    desc_tag = soup.find_all(class_='description')
    [i.clear() for i in desc_tag]

    # 处理基本信息：过滤数据，去掉空白
    intro_tag = soup.find('div', class_="lemma-summary")  # 获取百科基本信息列表
    intro_after_filter = re.sub('\n+', '', intro_tag.get_text())  # 去除换行
    # intro_after_filter = [''.join(i.split()) for i in intro_after_filter]  # 去除/0a乱码
    # 将字符串列表连成字符串并返回
    intro_after_filter = ''.join(intro_after_filter.split())
    # print(intro_after_filter)

    # 抽取信息框数据
    name_tag = soup.find_all('dt', class_="basicInfo-item name")  # 找到所有dt标签，返回一个标签列表
    value_tag = soup.find_all('dd', class_="basicInfo-item value")  # 找到所有dd标签，返回一个标签列表
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
        valuelist.append(value.strip('\n'))
    for i, j in zip(namelist,
                    valuelist):  # 多遍历循环，zip()接受一系列可迭代对象作为参数，将对象中对应的元素打包成一个个tuple（元组），然后返回由这些tuples组成的list（列表）。
        profile_info[i] = j
    # print(profile_info)

    # 抽取人物履历信息、担任职位、人物经历等所有栏目信息
    # 抽取鲶鱼效应等无标题的信息内容
    try:
        resume_tag = soup.find('div', class_=re.compile("para-title level-2"))  # 人物履历标签起点
        br_text_list = []
        title = resume_tag.find(class_='title-text').contents[1]
        # print(title)
        br_text_list.append('title-2: ' + title)
        for br in resume_tag.next_siblings:  # 获取人物履历标签后面所有的兄弟标签
            # print(br)
            if type(br) is bs4.element.Tag:  # 判断br是不是一个标签
                # 判断是否是栏目标题下的内容标签
                if br.name == 'div' and "class" in br.attrs:
                    attrs = ''.join(br.attrs['class'])
                    if attrs == 'para':
                        br_text = re.sub('\n+', '', br.get_text())
                        # print(br_text)
                        br_text_list.append(''.join(br_text.split()))
                    # 获取书籍信息
                    elif attrs == 'lemmaWgt-publication':
                        book_tag = br.find_all('li')
                        # print(book_info)
                        book_list = []
                        for b_li in book_tag:
                            # print(b_li)
                            book = {}
                            key_list = []
                            value_list = []
                            [key_list.append(re.sub('\n+', '', i.get_text())) for i in b_li.find_all(class_='item-key')]
                            # print(key_list)
                            [value_list.append(re.sub('\n+', '', j.get_text())) for j in
                             b_li.find_all(class_='item-value')]
                            # print(value_list)
                            book_info = re.sub('\n+', '', b_li.get_text())
                            book_name = value_list.pop(0)
                            # print(book_name)
                            book.update({'书名': book_name})
                            # print(book)
                            for i, j in zip(key_list, value_list):
                                book.update({i: j})

                            if book_info.endswith(value_list[-1]):
                                pass
                            else:
                                book_desc = book_info.split(value_list[-1])[-1]
                                book.update({'描述': book_desc})
                            book_list.append(book)
                        br_text_list.append(str(book_list))
                        # print(book_dict)
                    elif re.match(r'para-titlelevel-2', attrs):  # 当出现栏目2级标题时，获取标题名称
                        title = br.find(class_='title-text').contents[1]
                        # print(title)
                        br_text_list.append('title-2: ' + title)
                    elif re.match(r'para-titlelevel-3', attrs):  # 当出现栏目3级标题时，获取标题名称
                        title = br.find(class_='title-text').contents[1]
                        # print(title)
                        br_text_list.append('title-3: ' + title)
                # 下载表格数据
                elif br.name == 'table':
                    # print(br)
                    # 因为br是table-tag标签，所以需要用BeautifulSoup重新声明，以字符串形式
                    # br_soup = BeautifulSoup(str(br), 'lxml')
                    # print(type(br_soup))
                    # find_all()方法只能查找当前标签下的文本匹配标签
                    tr_list = br.find_all('tr')
                    for tr in tr_list:
                        tr_content = ''
                        # print(row)
                        for th in tr.contents:
                            if type(th) is bs4.element.Tag:
                                th_text = re.sub('\n', '', th.get_text())
                                tr_content += th_text + '\t'
                            else:
                                continue
                        # 使带"▪"的三级子标签换行
                        # if '▪' in tr_content:
                        # tr_content = re.sub('▪', '\n▪', tr_content).strip('\n')
                        # tr_content = tr_content + '\n'
                        # print(tr_content)
                        try:
                            # 删除爬取到html内容中的nbsp：str.replace(u'\xa0', u' ')
                            table_content = tr_content.replace(u'\xa0', u' ')
                            br_text_list.append(table_content.strip('\t') + '\n')
                        except Exception as e:
                            print(e)
            else:
                continue
    except AttributeError as e:
        print('AttributeError', e)

        for br in intro_tag.next_siblings:  # 获取人物履历标签后面所有的兄弟标签
            # print(br)
            if type(br) is bs4.element.Tag:  # 判断br是不是一个标签
                # 判断是否是栏目标题下的内容标签
                if br.name == 'div' and "class" in br.attrs:
                    attrs = ''.join(br.attrs['class'])
                    if attrs == 'para':
                        br_text = re.sub('\n+', '', br.get_text())
                        # print(br_text)
                        br_text_list.append(''.join(br_text.split()))

    # print(br_text_list)

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
    return intro_after_filter, profile_info, br_text_list, img_urllist



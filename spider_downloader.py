# -*- coding: UTF-8 -*-
# @Project -> File: python_spider_from_bdbaike -> spider_downloader
# @Time: 2021/6/8 16:49 
# @Author: Yu Yongsheng
# @Description: 将爬取的百度百科数据保存下来;

import os
from urllib.error import HTTPError

import requests
import xlrd
import xlwt
from xlutils.copy import copy
import json


# 下载爬到的数据：基本信息、信息框、图片
def download(name, intro, profile_dict, br_text_list, img_list):
    project_path = os.getcwd()
    # print('project_path:' + project_path)

    # 保存百科基本信息
    # if not os.path.exists('introduction'):
    #     os.mkdir('introduction')
    # introduction_file = project_path + '/introduction/' + name + '.json'
    # print(introduction_file)
    # with open(introduction_file, 'w', encoding='utf-8') as f:
        # 转换成json格式输出
    intro_dict = {'基本信息': intro}
        # 防止json编码时中文ascii乱码，用ensure_ascii=False
        # intro_dict_json = json.dumps(intro_dict, indent=4, ensure_ascii=False)

        # f.write(intro_dict_json + '\n')
    # print('introduction输出完毕')

    # 将信息框数据以json格式输出
    # with open(introduction_file, 'a+') as f:
        # profile_dict_json = json.dumps(profile_dict, indent=4, ensure_ascii=False, sort_keys=False)
        # f.write(profile_dict_json + '\n')
    '''
    # 保存信息框数据到excel
    if not os.path.exists('profile'):
        os.mkdir('profile')

    profile_file = project_path + '/profile/' + 'profile.csv'
    field_list = ['中文名', '外文名', '别名', '性别', '学位', '职称', '国籍', '民族', '出生地', '籍贯', '出生日期', '逝世日期',
                  '星座', '血型', '身高', '体重', '毕业院校', '职业', '经纪公司', '代表作品', '主要成就', '生肖', '语种', '特长', '粉丝名']
    if not os.path.exists(profile_file):
        workbook = xlwt.Workbook(encoding='utf-8')
        output_sheet = workbook.add_sheet('profile_sheet', cell_overwrite_ok=True)
        for i in range(len(field_list)):
            output_sheet.write(0, i, field_list[i])
        workbook.save(profile_file)

    rb = xlrd.open_workbook(profile_file)
    rows_num = rb.sheet_by_name('profile_sheet').nrows
    # print(rows_num)
    wb = copy(rb)
    output_sheet = wb.get_sheet(0)
    # print(profile)
    for i in range(len(field_list)):
        if profile_dict.get(field_list[i]):
            output_sheet.write(rows_num, i, profile_dict.get(field_list[i]))
        else:
            continue
    os.remove(profile_file)
    wb.save(profile_file)
    '''

    # 保存人物履历、职务、研究等栏目内容到基本信息.txt中
    # api返回json数据，在web中进行展示
    cv_output = {}
    # with open(introduction_file, 'a+') as f:
    # print(br_text_list)
    # 转换成json格式输出
    key_2 = ''
    value = ''
    key_3 = ''
    output_dict_2 = {}
    output_dict_3 = {}
    for i in range(len(br_text_list)):
        # print(i)
        item = br_text_list[i]
        if isinstance(item, str):
            # 2级标题
            if item.startswith('title-2'):
                key_2 = item.split(': ')[1]
                # continue
            # 3级标题
            elif item.startswith('title-3'):
                key_3 = item.split(': ')[1]
                # continue
            else:
                value += item

            # 根据下一索引的值判断第2级标题还是第3级标题，然后返回字典形式的内容
            if i+1 < len(br_text_list):
                if br_text_list[i+1].startswith('title-3'):
                    if key_3:
                        output_dict_3.update({key_3: value})
                        key_3 = ''
                        value = ''
                        continue
                elif br_text_list[i+1].startswith('title-2'):
                    if key_3:
                        output_dict_3.update({key_3: value})
                        output_dict_2 = {key_2: output_dict_3}
                        cv_output.update(output_dict_2)
                        # output_dict_2_json = json.dumps(output_dict_2, indent=4, ensure_ascii=False)
                        # f.write(output_dict_2_json + '\n')
                        key_3 = ''
                        value = ''
                        output_dict_2 = {}
                        output_dict_3 = {}
                        continue
                    else:
                        output_dict_2 = {key_2: value}
                        cv_output.update(output_dict_2)
                        # output_dict_2_json = json.dumps(output_dict_2, indent=4, ensure_ascii=False)
                        # f.write(output_dict_2_json + '\n')
                        value = ''
                        output_dict_2 = {}
                        continue
                else:
                    continue
            else:
                value = value + br_text_list[-1]
                if key_3:
                    output_dict_3.update({key_3: value})
                    output_dict_2 = {key_2: output_dict_3}
                else:
                    output_dict_2 = {key_2: value}
                cv_output.update(output_dict_2)
                # output_dict_2_json = json.dumps(output_dict_2, indent=4, ensure_ascii=False)
                # f.write(output_dict_2_json + '\n')
        # 输出字典格式的图书信息
        elif isinstance(item, list):
            cv_output.update({key_2: item})
            # output = json.dumps({key_2: item}, indent=4, ensure_ascii=False)
            # f.write(output)
            continue
    print('人物履历输出完毕')


    # 保存图片
    # 请求头部，伪造浏览器，防止爬虫被反
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    download_limit = 10  # 单个人物下载的最大图片数
    if not os.path.exists('img'):
        os.mkdir('img')
    name_path = project_path + '/img/' + name
    if not os.path.exists(name_path):
        os.mkdir(name_path)

    count = 1
    for img_url in img_list:
        try:
            response = requests.get(img_url, headers=headers)  # 得到访问的网址
            content = response.content
            filename = name_path + '/' + name + '_%s.png' % count
            with open(filename, "wb") as f:
                # 如果图片质量太差，跳过
                if len(content) < 1000:
                    continue
                f.write(content)  # 保存图片
            response.close()
            count += 1
            # 每个模特最多只下载download_limit张
            if count > download_limit:
                break

        except HTTPError as e:  # HTTP响应异常处理
            print(e.reason)

    return intro_dict, profile_dict, cv_output
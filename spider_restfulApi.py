
# -*- coding: UTF-8 -*-
# @Project -> File: python_spider_from_bdbaike -> spider_baike_text_picture
# @Time: 2021/6/3 20:13
# @Author: Yu Yongsheng
# @Description: 从百度百科爬取人物的基本信息、信息框数据和图片

import json
import spider_claw
import spider_downloader
# 安装Restful package
from flask import Flask, request, jsonify
from flask_restful import reqparse, abort, Api, Resource


# 防止ssl报错
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 初始化app, api
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/<name>')
def home(name):
    # 去除favicon.ico干扰
    if name =="favicon.ico":
        pass
    else:
        intro, profile_dict, br_text_list, img_list = spider_claw.claw(name)
        intro_dict, profile_dict, cv_output = spider_downloader.download(name, intro, profile_dict, br_text_list, img_list)
        output = [intro_dict, profile_dict, cv_output]
        intro_dict_json = json.dumps(output, indent=4, ensure_ascii=False)

        return intro_dict_json

if __name__ == '__main__':
    # 设置ip、端口
    # app.run(host='127.0.0.1', port=8891)
    app.run()

    # trigger = True
    # while (trigger):
    #     name = '潘建伟'  # input('查询词语：')
    #     intro, profile_dict, br_text_list, img_list = spider_claw.claw(name)
    #     spider_downloader.download(name, intro, profile_dict, br_text_list, img_list)
    # #     # print("查询结果：%s" % result)
    #     trigger = False




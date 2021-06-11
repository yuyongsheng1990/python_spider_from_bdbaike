# -*- coding: UTF-8 -*-
# @Project -> File: python_spider_from_bdbaike -> spider_baike_text_picture
# @Time: 2021/6/3 20:13 
# @Author: Yu Yongsheng
# @Description: 从百度百科爬取人物的基本信息、信息框数据和图片

import spider_claw
import spider_downloader
# 防止ssl报错
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


if __name__ == '__main__':
    trigger = True
    while (trigger):
        name = '潘建伟'  # input('查询词语：')
        intro, profile_dict, br_text_list, img_list = spider_claw.claw(name)
        spider_downloader.download(name, intro, profile_dict, br_text_list, img_list)
        # print("查询结果：%s" % result)
        trigger = False




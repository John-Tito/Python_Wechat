#coding=utf-8
import json
import math
import os
import re
from collections import Counter

import jieba.analyse
from PIL import Image, ImageFilter
from pyecharts import Bar, Map, Pie, WordCloud


#graph_tittle为标题兼文件名，name_list为项目列表，value_list为词频数据
#条形图
def get_bar(graph_tittle, name_list, value_list):
    bar = Bar(title=graph_tittle)
    bar.add("", name_list, value_list)
    file_name = graph_tittle + ".html"
    bar.render(file_name)

#饼状图
def get_pie(graph_tittle, name_list, value_list):
    pie = Pie(title=graph_tittle)
    pie.add("", name_list, value_list, is_lable_show=True)
    file_name = graph_tittle + ".html"
    pie.render(file_name)

#地图
def get_map(graph_tittle, name_list, value_list):
    map = Map(title=graph_tittle)
    map.add(
        "", name_list, value_list, is_visualmap=True, visual_text_color="#000")
    file_name = graph_tittle + ".html"
    map.render(file_name)

#词云
def get_wordCloud(graph_tittle, name_list, value_list):
    wordClould = WordCloud(title=graph_tittle)
    wordClould.add(
        "",
        name_list,
        value_list,
        shape="circle",
        word_gap=20,
        word_size_range=None,
        rotate_step=45)
    file_name = graph_tittle + ".html"
    wordClould.render(file_name)

#关键词提取
def get_tag(text, counter):
    print('analysizing:' + text)
    tag_list = jieba.analyse.extract_tags(text)
    for tag in tag_list:
        if tag != "":
            counter[tag] += 1
        else:
            counter['blank'] += 1


def get_mergeImage(width_height):
    mkpath("/img")
    dirName = os.getcwd()
    photo_path_list = []
    for root, dirs, files in os.walk(dirName):
        for file in files:
            if "jpg" in file and os.path.getsize(os.path.join(root, file)) > 0:
                photo_path_list.append(os.path.join(root, file))

    length = len(photo_path_list)
    max_raw = math.floor(math.sqrt(length)) + 1
    if (length % max_raw == 0):
        max_line = length / max_raw
    else:
        max_line = math.floor(length / max_raw) + 1

    img_final = Image.new(
        "RGB", (max_raw * width_height, max_line * width_height), "white")

    num = 0
    for line in range(0, max_line):
        if num >= length:
            break
        for raw in range(0, max_raw):
            x = raw * width_height
            y = line * width_height
            if num >= length:
                break
            name = photo_path_list[num]
            f_img = Image.open(name)
            f_img_copy = f_img.resize((width_height, width_height),
                                      Image.ANTIALIAS)
            img_final.paste(f_img_copy, (x, y))
            num += 1
    os.chdir("..")
    mkpath("/analyse")
    img_final.save('merged.png')
    os.chdir("..")
    img_final.show()


#创建并切换目录
def mkpath(m_path):
    path = os.getcwd() + m_path
    path = path.strip()
    is_exists = os.path.exists(path)
    if is_exists:
        print(path, 'path is exits')
    else:
        print('create a path names', path)
        os.makedirs(path)
    os.chdir(path)


#将counter转换为两个列表
def counter2list(counter):
    name_list = []
    value_list = []
    for name, value in counter.items():
        name_list.append(name)
        value_list.append(value)
    return name_list, value_list


mkpath("/json")
with json.codecs.open("friend.json", encoding='utf-8') as f:
    friensds = json.load(f)
os.chdir("..")

sex_counter = Counter()
Province_counter = Counter()
Signature_counter = Counter()
NickName_list = []

for friend in friensds:
    sex_counter[friend['Sex']] += 1
    if friend['Province'] != "":
        Province_counter[friend['Province']] += 1
    NickName_list.append(friend['NickName'])
    get_tag(friend['Signature'], Signature_counter)
    get_tag(friend['NickName'], Signature_counter)
#这里把昵称也一同加入到了签名里面生成云图

#生成性别饼图
mkpath("/analyse")
name_list, value_list = counter2list(sex_counter)
get_pie("sex", name_list, value_list)

#生成地理分布柱形图及地图
name_list, value_list = counter2list(Province_counter)
get_bar("province_bar", name_list, value_list)
get_map("province_map", name_list, value_list)

#生成昵称及签名云图
name_list, value_list = counter2list(Signature_counter)
get_wordCloud("signature", name_list, value_list)
os.chdir("..")

get_mergeImage(50)

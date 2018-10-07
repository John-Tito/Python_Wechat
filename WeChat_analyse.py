
#coding=utf-8
from pyecharts import Bar
from pyecharts import Pie
from pyecharts import Map
from pyecharts import WordCloud
from collections import Counter
import re
import os
import json
import jieba.analyse

#graph_tittle为标题兼文件名，name_list为项目列表，value_list为词频数据
#条形图
def get_bar(graph_tittle, name_list, value_list):
    bar = Bar(title=graph_tittle)
    bar.add("", name_list, value_list)
    file_name = graph_tittle + ".html"
    bar.render(file_name)
#饼状图
def get_pie(graph_tittle,name_list, value_list):
    pie = Pie(title=graph_tittle)
    pie.add("", name_list, value_list, is_lable_show=True)
    file_name = graph_tittle + ".html"
    pie.render(file_name)
#地图
def get_map(graph_tittle, name_list, value_list):
    map =Map(title=graph_tittle)
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
def get_tag(text,counter):
    print('analysizing:'+text)
    tag_list = jieba.analyse.extract_tags(text)
    for tag in tag_list:
        if tag!="":
            counter[tag]+=1
        else:
            counter['blank']+=1
#创建并切换目录
def mkdir():
    path = "D:/Test/head_img"
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
    return name_list,value_list

mkdir()
with json.codecs.open("D:/Test/head_img/friend.json", encoding='utf-8') as f:
    friensds = json.load(f)
sex_counter = Counter()
Province_counter = Counter()
Signature_counter = Counter()
NickName_list = []

for friend in friensds:
    sex_counter[friend['Sex']]+=1
    if friend['Province']!="":
        Province_counter[friend['Province']]+=1
    NickName_list.append(friend['NickName'])
    get_tag(friend['Signature'],Signature_counter)
    get_tag(friend['NickName'], Signature_counter)
#这里把昵称也一同加入到了签名里面生成云图

#生成性别饼图
name_list, value_list = counter2list(sex_counter)
get_pie("sex", name_list, value_list)

#生成地理分布柱形图及地图
name_list, value_list = counter2list(Province_counter)
get_bar("province_bar", name_list, value_list)
get_map("province_map", name_list, value_list)

#生成昵称及签名云图
name_list, value_list = counter2list(Signature_counter)
get_wordCloud("signature", name_list, value_list)

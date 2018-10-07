#wechat test
#coding=utf-8
import itchat
import os
import json

#创建文件夹，切换操作目录
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

#根据userName获取并保存头像图片
def save_head(name,i):
    img = itchat.get_head_img(userName=name)
    print('start saving image')
    file_name = str(i) + '.jpg'
    print('start saving file')
    with open(file_name, 'ab') as f:
        f.write(img)
        print(file_name, 'successfully saved')

#保存所需的信息到friend.json
def save_info(friends_info):
    mkdir()
    file_name = "friend.json"
    print('start saving data')
    with json.codecs.open(file_name, 'ab', encoding='utf-8') as f:
        f.write(json.dumps(friends_info,ensure_ascii=False))
        print(file_name, 'successfully saved')

#批量获取头像
def get_pic(friends_info):
    mkdir()
    i=1
    for friend_info in friends_info:
        save_head(friend_info['UserName'], i)
        i+=1

def get_info(friend_list):
    sex_dict = {}
    sex_dict['0'] = "其他"
    sex_dict['1'] = "男"
    sex_dict['2'] = "女"
    friends_info =[]
    for friend in friend_list:
        item = {}
        item['NickName'] = friend['NickName']
        item['HeadImgUrl'] = friend['HeadImgUrl']
        item['Sex'] = sex_dict[str(friend['Sex'])]
        item['Province'] = friend['Province']
        item['Signature'] = friend['Signature']
        item['UserName'] = friend['UserName']
        friends_info.append(item)
    save_info(friends_info)
    get_pic(friends_info)


if itchat.check_login()!=200:
    itchat.auto_login(hotReload=True)
get_info(itchat.get_friends(update=True))

# -*-coding:utf-8-*-
import web
import socket
import random
from EatYourFood import ConnectToSQL as sql
from EatYourFood.工具 import dict2json as dj
render = web.template.render('templates')

class ChangeUserInfo(object):
    def POST(self):
        print('ChangeUserInfo POST')
        web.header("Access-Control-Allow-Origin", "*")
        web.header('Access-Control-Allow-Headers', '*')
        # web.header('content-type', 'text/json')
        web.header('content-type', 'mulitpart/form-data')
        web_info = web.input()

        ID = web_info['userid']
        name = web_info['username']
        location = web_info['location']
        cell = web_info['cellPhoneNumber']
        profile = web_info['profile']

        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)

        data = web_info['imgFile']

        if data == 'undefined':
            search_order = "select u_img from users where u_id='%s'" % (ID)
            oldImg = list(sql.search(search_order)[0])[0]
            print('不改变-oldImg',oldImg)
            print('不改变-oldImg', oldImg)

            update_order = "update users set u_name='%s', u_loca='%s',u_cell='%s',u_profile='%s',u_img='%s' where u_id='%s'" % (
            name, location, cell, profile, oldImg, ID)

            sql.update(update_order)
            return{'code':1,'avatar':oldImg}

        version = random.randint(1,1000000)
        filename = 'UserPicture_%s_%s.jpg' % (ID,str(version))


        filedir_local = './static'
        fout = open(filedir_local + '/' + filename, 'wb')
        fout.write(bytes(data))
        fout.close()

        filedir = 'http://' + str(ip) + ':8080/static'
        imgFile = filedir + '/' + filename

        print('修改后-imgfile',imgFile)
        print('修改后-imgfile',imgFile)

        print('修改后')
        print('ID:',ID)
        print('name:',name)
        print('location:',location)
        print('cellPhoneNumber:',cell)
        print('profile:',profile)
        print('image',imgFile)

        update_order = "update users set u_name='%s', u_loca='%s',u_cell='%s',u_profile='%s',u_img='%s' where u_id='%s'" % (name,location,cell,profile,imgFile,ID)

        sql.update(update_order)
        return dj.ToJson({'code':1,'avater':imgFile})

















# flag = ''
# ID = ''
# with open('当前ID信息.txt','r',encoding='utf-8') as f:
#     for line in f.readlines():
#         tok = line.strip().split()
#         flag = tok[0]
#         ID = tok[1]
# if not ID:
#     return render.notfound()
#
# print("用户ID获取成功")
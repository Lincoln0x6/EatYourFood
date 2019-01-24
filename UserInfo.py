# -*-coding:utf-8-*-
import web
import socket
from EatYourFood import ConnectToSQL as sql
from EatYourFood.工具 import dict2json as dj
render = web.template.render('templates')

class UserInfo(object):
    def GET(self):
        print('UserInfo GET')
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'text/json')
        # flag = ''
        # ID = ''
        # with open('当前ID信息.txt','r',encoding='utf-8') as f:
        #     for line in f.readlines():
        #         tok = line.strip().split()
        #         flag = tok[0]
        #         ID = tok[1]
        # if not ID:
        #     return render.notfound()
        # print("用户ID获取成功")

        web_info = web.input()

        ID = web_info['userid']

        search_order = "select u_name,u_cell,u_loca,u_profile,u_img,u_vipstatus from users where u_id='%s'" % (ID)

        record = sql.search(search_order)

        if not record:
            return render.notfound()

        print('返回的用户信息为',record)
        name,cell,location,profile,img,vipstatus = record[0]
        # print("从数据库返回的图片地址为",img)
        #
        # if img == 'undefined':
        #     hostname = socket.gethostname()
        #     ip = socket.gethostbyname(hostname)
        #     img = 'http://' + str(ip) + '/static' + 'UserPicture_%s' % (ID)

        dictReturn = {
            "userid": ID,
            "username": name,
            "cellPhoneNumber": cell,
            "location": location,
            "profile": profile,
            "avater": img,
            "vipstatus":vipstatus,
        }

        return dj.ToJson(dictReturn)
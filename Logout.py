# -*-coding:utf-8-*-
import web
from EatYourFood import ConnectToSQL as sql
from EatYourFood.工具 import dict2json as dj

class Logout(object):
    def POST(self):
        print('Logout POST')
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'text/json')
        web_info = web.input()
        uid = web_info['uid']
        if web_info['index'] == '1':
            update_order = "update users set u_isonline='%s' where u_id = '%s'" % ('0',uid)
            sql.update(update_order)
            print(uid, '退出登录')
        return dj.ToJson({'index':1})
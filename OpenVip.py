# -*-coding:utf-8-*-
import web
from EatYourFood import ConnectToSQL as sql
from EatYourFood.工具 import dict2json as dj

class OpenVip(object):
    def POST(self):
        print('OpenVip POST')
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'text/json')
        vipNumber = ['v123','v321']
        web_info = web.input()
        number =  web_info['vipNumber']
        userid = web_info['userid']
        search_order = "select u_vipstatus from users where u_id = '%s'" % (userid)
        currentVipStatus = int(sql.search(search_order)[0][0])

        if number not in vipNumber:
            return dj.ToJson({"code":-1})
        elif currentVipStatus != 0:
            return dj.ToJson({"code":0})
        else:
            update_order = "update users set u_vipstatus = '6' where u_id = '%s'" % (userid)
            sql.update(update_order)
            print(userid,"<--->成功开通vip")
            return dj.ToJson({"code":1})

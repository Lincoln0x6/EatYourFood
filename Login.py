# -*-coding:utf-8-*-
import web
from EatYourFood import ConnectToSQL as sql
from EatYourFood.工具 import dict2json as dj
from EatYourFood.工具 import i_p_isvaild as ipvd

class Login(object):
    def POST(self):
        print('Login POST')
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'text/json')
        web_info = web.input()
        #index为0是用户
        if web_info['index'] == '0':
            id_psw = {}
            id_status = {}
            search_order = 'select u_id,u_psw,u_isonline from users'
            records = sql.search(search_order)

            if not records:
                print('数据库用户表为空')
                return dj.ToJsonLogin(-2)

            for i in range(len(records)):
                id_psw[records[i][0]] = ipvd.pswDecode(records[i][1])
                id_status[records[i][0]] = records[i][2]
            web_id = web_info['userid']
            web_psw = web_info['password']

            if web_id not in id_psw:
                print('该用户ID不存在')
                return dj.ToJsonLogin(-1)

            if web_psw == id_psw[web_id]:
                if id_status[web_id] == '1':
                    print(web_id,'用户已登录')
                    return dj.ToJsonLogin(-3)
                print('用户登陆成功')
                print('当前用户登陆id为', web_info['userid'])
                update_order = "update users set u_isonline='%s' where u_id = '%s'" % ('1',web_info['userid'])
                sql.update(update_order)
                # with open('当前ID信息.txt','w',encoding='utf-8') as f:
                #     f.write(str(web_info['index']) + ' ' + web_info['userid'])
                #     print('ID信息成功保存')
                return dj.ToJsonLogin(1)
            else:
                print('用户密码错误')
                return dj.ToJsonLogin(0)


        # index为1是商家
        elif web_info['index'] == '1':

            id_psw = {}

            search_order = 'select s_id,s_psw from seller'
            records = sql.search(search_order)

            if not records:
                print('数据库商家表为空')
                return dj.ToJsonLogin(-2)

            for i in range(len(records)):
                id_psw[records[i][0]] = ipvd.pswDecode(records[i][1])

            web_id = web_info['sellid']
            web_psw = web_info['password']

            if web_id not in id_psw:
                print('该商家ID不存在')
                return dj.ToJsonLogin(-1)

            if web_psw == id_psw[web_id]:
                print('商家登陆成功')
                print('当前商家登陆id为', web_info['sellid'])
                with open('当前ID信息.txt','w',encoding='utf-8') as f:
                    f.write(str(web_info['index']) + ' ' + web_info['sellid'])
                    print('ID信息成功保存')
                return dj.ToJsonLogin(1)
            else:
                print('商家登陆密码错误')
                return dj.ToJsonLogin(0)
        else:
            print('接口错误')


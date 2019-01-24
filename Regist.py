# -*-coding:utf-8-*-
import web
import socket
import traceback
from EatYourFood import ConnectToSQL as sql
from EatYourFood.工具 import dict2json as dj
from EatYourFood.工具 import i_p_isvaild as ipvd

class Regist(object):
    def POST(self):
        print('Regist POST')
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'text/json')
        web_info = web.input()
        # print(type(web_info['index']))
        #index为0是用户
        if web_info['index'] == '0':
            id = set()
            cell = set()

            records = sql.search('select u_id,u_cell from users')

            #判断输入是否为空
            if not web_info['userid']:
                print('用户ID为空')
                return dj.ToJsonRegist(-6)
            if not web_info['password']:
                print('密码为空')
                return dj.ToJsonRegist(-5)
            # if not web_info['password1'] or not web_info['password2']:
            #     print('用户密码为空')
            #     return dj.ToJsonRegist(-5)
            if not web_info['cell']:
                print('用户电话号码为空')
                return dj.ToJsonRegist(-4)

            #检查id是否合法
            if not ipvd.idIsVaild(web_info['userid']):
                print('用户id不合法')
                return dj.ToJsonRegist(-7)

            # #判断两次输入的密码是否一致
            # if web_info['password1'] != web_info['password2']:
            #     print('用户两次输入的密码不一致')
            #     return dj.ToJsonRegist(-2)

            # 检查密码是否合法
            if not ipvd.pswIsVaild(web_info['password']):
                print('用户密码不合法')
                return dj.ToJsonRegist(-8)

            #获取数据库已有的id和cell
            for i in range(len(records)):
                id.add(records[i][0])
                cell.add(records[i][1])
            #判断id和cell是否重复
            if web_info['userid'] in id:
                print('用户名已存在')
                return dj.ToJsonRegist(-1)
            if web_info['cell'] in cell:
                print('用户电话号码已存在')
                return dj.ToJsonRegist(0)

            try:

                hostname = socket.gethostname()
                ip = socket.gethostbyname(hostname)

                filename1 = 'UserPictureDefault.jpg'

                filedir = 'http://' + str(ip) + ':8080/static'

                imgFile = filedir + '/' +filename1

                insert_order = "insert into users values('%s','','%s','%s','','','%s','%s','%s')" % (
                web_info['userid'], ipvd.pswEncode(web_info['password']),
                web_info['cell'],imgFile,'0','0')

                isSucc = sql.insert(insert_order)
                if isSucc:
                    print('用户注册成功')
                    return dj.ToJsonRegist(1)
                else:
                    print('用户注册失败')
                    return dj.ToJsonRegist(-9)
            except:
                print('用户注册失败 请看错误日志2')
                f = open("errorlog2.txt", 'a')
                traceback.print_exc(file=f)
                f.flush()
                f.close()
                return dj.ToJsonRegist(-9)
        # code为1是商家
        elif web_info['index'] == '1':

            id = set()
            cell = set()

            records = sql.search('select s_id,s_cell from seller')

            # 判断输入是否为空
            if not web_info['sellid']:
                print('商家ID为空')
                return dj.ToJsonRegist(-6)
            # if not web_info['password']:
            #     print('密码为空')
            #     return dj.ToJsonRegist(-5)
            if not web_info['password1'] or not web_info['password2']:
                print('商家密码为空')
                return dj.ToJsonRegist(-5)
            if not web_info['cell']:
                print('商家电话号码为空')
                return dj.ToJsonRegist(-4)

            # 检查id是否合法
            if not ipvd.idIsVaild(web_info['sellid']):
                print('商家id不合法')
                return dj.ToJsonRegist(-7)

            # 判断两次输入的密码是否一致
            if web_info['password1'] != web_info['password2']:
                print('商家两次输入的密码不一致')
                return dj.ToJsonRegist(-2)

            # 检查密码是否合法
            if not ipvd.pswIsVaild(web_info['password1']):
                print('商家密码不合法')
                return dj.ToJsonRegist(-8)

            # 获取数据库已有的id和cell
            for i in range(len(records)):
                id.add(records[i][0])
                cell.add(records[i][1])
            # 判断id和cell是否重复
            if web_info['sellid'] in id:
                print('商家名已存在')
                return dj.ToJsonRegist(-1)
            if web_info['cell'] in cell:
                print('商家电话号码已存在')
                return dj.ToJsonRegist(0)

            try:
                insert_order = "insert into seller values('%s','','%s','','','%s',0,0,0,0,'')" % (
                                web_info['sellid'], ipvd.pswEncode(web_info['password1']),
                                web_info['cell'])

                isSucc = sql.insert(insert_order)
                if isSucc:
                    print('商家注册成功')
                    return dj.ToJsonRegist(1)
                else:
                    print('商家注册失败')
                    f = open("错误日志/errorlog4.txt", 'a')
                    traceback.print_exc(file=f)
                    f.flush()
                    f.close()
                    return dj.ToJsonRegist(-9)
            except:
                print('商家注册失败 请看错误日志3')
                f = open("错误日志/errorlog3.txt", 'a')
                traceback.print_exc(file=f)
                f.flush()
                f.close()

        else:
            print('接口错误')


# -*-coding:utf-8-*-
import web
import datetime
from EatYourFood import ConnectToSQL as sql
from EatYourFood.工具 import dict2json as dj

class Order(object):
    def POST(self):
        print('Order POST')
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'text/json')
        web_info = web.input()
        web_info = dj.ToDict(web_info['data'])

        ordNum = []
        with open('当前总订单数.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                ordNum.append(line.strip())
        print('当前总订单数为', ordNum[0])

        orderid = "order_%s" % (ordNum[0])
        print('当前订单号', orderid)

        currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        order_status = '接单中'

        userid = web_info['userid']
        dishInfo = web_info['food']

        dishidList = []
        dish_Idcount_Dict = {}

        for i in range(len(dishInfo)):
            dishidList.append(dishInfo[i]['dishid'])
            dish_Idcount_Dict[dishidList[i]] = dishInfo[i]['count']

        print(dishidList)
        print(dish_Idcount_Dict)


        search_order = "select d_sid from dish where d_id='%s'" % (dishidList[0])
        sellid = list(sql.search(search_order)[0])[0]

        dishid = ''
        for i in range(len(dishidList)):
            dishid = dishid + dishidList[i] + ' '
            update_order = "update dish set d_ordnum='%s' where d_id='%s'" % (
            dish_Idcount_Dict[dishidList[i]], dishidList[i])
            sql.update(update_order)

        for i in range(len(dishidList)):
            search_order = "select d_left from dish where d_id='%s'" % (dishidList[i])
            oldLeft = list(sql.search(search_order)[0])[0]
            newLeft = oldLeft - dish_Idcount_Dict[dishidList[i]]
            update_order = "update dish set d_left='%s' where d_id='%s'" % (newLeft,dishidList[i])
            sql.update(update_order)

        dishid = dishid.strip()

        search_order = "select u_cell,u_loca from users where u_id='%s'" % (userid)
        cell, location = sql.search(search_order)[0]

        insert_order = "insert into orders values('%s','%s','%s','%s','%s','%s','%s','%s')" % (
            orderid, order_status, userid, sellid, dishid, location, cell, currentTime)
        isSuccess = sql.insert(insert_order)

        if isSuccess:
            print('订单插入成功')
            if web_info['use'] == '1':
                #在这里加入刷新vipstatus
                search_order = "select u_vipstatus from users where u_id = '%s'" % (userid)
                currentVipStatus = int(sql.search(search_order)[0][0])
                if currentVipStatus > 0:
                    newVipStatus = str(currentVipStatus - 1)

                    update_order = "update users set u_vipstatus = '%s' where u_id = '%s'" % (newVipStatus,userid)
                    sql.update(update_order)

            with open('当前总订单数.txt', 'w', encoding='utf-8') as f:
                newNum = int(ordNum[0]) + 1
                f.write(str(newNum))
            return dj.ToJson({"code":1})
        else:
            print('订单插入失败')


# dict = {
#     "userid":'u001',
#     "food":[
#         {
#             "dishid":'d001',
#             "count": 12,
#         },
#         {
#             "dishid":'d002',
#             "count": 10,
#         }
#     ]
# }


# -*-coding:utf-8-*-
import web
from EatYourFood.工具 import dict2json as dj
from EatYourFood import ConnectToSQL as sql

class SellDishInfo(object):
    def returnFoodDict(self,id,name,profile,discount,price,left,score,orderedNumber,image):
        foodDict = {
          "id": id,
          "name": name,
          "profile": profile,
          "discount": float(discount),
          "price": float(price),
          "left": float(left),
          "score": float(score),
          "orderedNumber": float(orderedNumber),
          "image": image,
        }
        return foodDict

    def returnSellDict(self,id, name, psw, profile, location, cell, score, status, min, de, image, foods):
        sellDict = {
            "id": id,
            "name": name,
            "password": psw,
            "profile": profile,
            "location": location,
            "cellPhoneNumber": cell,
            "score": float(score),
            "status": float(status),
            "minPrice": float(min),
            "delivePrice": float(de),
            "image": image,
            "foods": foods,
        }
        return sellDict


    def returnBigDict(self,all):
        bigDict = {
            "seller": all,
        }
        return bigDict

    def GET(self):
        print('SellDishInfo GET')
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'text/json')
        search_order1 = 'select s_id from seller'
        sellid = sql.search(search_order1)
        for i in range(len(sellid)):
            sellid[i] = list(sellid[i])[0]

        sellList = []

        for i in range(len(sellid)):
            currentID = sellid[i]

            search_order2 = "select s_name,s_psw,s_profile,s_loca,s_cell,s_score,s_status,s_minpe,s_delive,s_img from seller where s_id='%s'" % (
                currentID)
            sellInfo = sql.search(search_order2)

            search_order3 = "select d_id,d_name,d_profile,d_discount,d_price,d_left,d_score,d_ordnum,d_img from dish where d_sid='%s'" % (
                currentID)
            dishInfo = sql.search(search_order3)
            foodList = []

            for dishNum in range(len(dishInfo)):
                d_id, d_name, d_profile, d_discount, d_price, d_left, d_score, d_ordnum, d_img = dishInfo[dishNum]
                foodList.append(
                    self.returnFoodDict(d_id, d_name, d_profile, d_discount, d_price, d_left, d_score, d_ordnum, d_img))

            s_name, s_psw, s_profile, s_loca, s_cell, s_score, s_status, s_minpe, s_delive, s_img = sellInfo[0]

            sellList.append(
                self.returnSellDict(currentID, s_name, s_psw, s_profile, s_loca, s_cell, s_score, s_status, s_minpe,
                               s_delive, s_img, foodList))

            foodList = []
        print('商家表建立成功 商家和菜品信息已成功返回')
        return dj.ToJson(self.returnBigDict(sellList))

# print(SellDishInfo().GET()['seller'][0]['foods'][1]['name'])
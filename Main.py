# -*-coding:utf-8-*-
import web
from EatYourFood.Login import Login
from EatYourFood.Logout import Logout
from EatYourFood.Regist import Regist
from EatYourFood.SellDishInfo import SellDishInfo
from EatYourFood.UserInfo import UserInfo
from EatYourFood.ChangeUserInfo import ChangeUserInfo
from EatYourFood.Order import Order
from EatYourFood.OpenVip import OpenVip
render = web.template.render('templates')

urls = (
    '/Login','Login',
    '/Regist','Regist',
    '/SellDishInfo','SellDishInfo',
    '/UserInfo','UserInfo',
    '/ChangeUserInfo','ChangeUserInfo',
    '/Order','Order',
    '/Logout','Logout',
    '/OpenVip','OpenVip',
    '/.*', 'Others',
)

class Others(object):
    def GET(self):
        return render.notfound()

app = web.application(urls, globals())

if __name__ == '__main__':
    print('Main is running')
    app.run()
# -*-coding:utf-8-*-
import pymssql
import traceback

def get_cur():
    try:
        conn = pymssql.connect(host='.', database='EatYourFood')
        cursor = conn.cursor()
    except:
        print('数据库连接失败')
    return conn,cursor

def search(search_order):
    _,cur = get_cur()
    cur.execute(search_order)
    return cur.fetchall()


def insert(insert_order):
    conn,cur = get_cur()
    try:
        cur.execute(insert_order)
        print('插入指令成功执行')
        conn.commit()
        print('数据库成功更新')
        return True
    except:
        print('插入失败 请看错误日志1')
        f = open("错误日志/errorlog1.txt", 'a')
        traceback.print_exc(file=f)
        f.flush()
        f.close()
        return False

def update(update_order):
    conn,cur = get_cur()
    cur.execute(update_order)
    print('更新指令成功执行')
    conn.commit()
    print('数据库成功更新')

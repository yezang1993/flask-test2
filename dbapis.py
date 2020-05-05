import datetime
import json
from operator import itemgetter
from typing import List, Tuple

from db import create_connection

from models import UserAccount, Shop,Messages


def regist_user(user:UserAccount)->UserAccount:
    db = create_connection()
    con = db.cursor()
    try:
        con.execute('insert into users(username, password) values(%s, %s)', (user.username, user.password))
        db.commit()
        db.close()
        con.close()
        return user
    except:
        db.rollback()
        db.close()
        con.close()

def login_user(username,  password)->UserAccount:
    db = create_connection()
    con = db.cursor()
    con.execute('select username,password from users where username=%s and password=%s', (username, password))
    s = con.fetchone()
    con.close()
    db.close()
    if s:
        return UserAccount(s[0], s[1])

def get_all_shop()->List[Shop]:
    db = create_connection()
    con = db.cursor()
    con.execute('select * from infoshop ')
    s = con.fetchall()

    con.close()
    db.close()
    Shops = []
    for item in s:
       Shops.append(item)
    return Shops


def get_Shop_by_id(inshopid) -> Shop:
    db = create_connection()
    con = db.cursor()

    con.execute("select * from infoshop where shopunid='%d'"% int(inshopid))
    s = con.fetchone()
    con.close()
    db.close()
    if s:
        return Shop(s[4], s[1], s[3], s[2],s[0])
    pass

def get_result_search(keyword):
    db = create_connection()
    con = db.cursor()
    re=[];
    con.execute("select * from infoshop where shopname like '%%%s%%'"% keyword)
    s = con.fetchall()
    for item in s:
        re.append(item)

    con.close()
    db.close()
    return re


def get_all_mess(inshopid)->List[Messages]:
    db = create_connection()
    con = db.cursor()
    con.execute("select * from comments where shopunid='%d'"% int(inshopid))
    s = con.fetchall()

    con.close()
    db.close()
    Mess = []
    for item in s:
       Mess.append(item)
    return Mess

def mess_add(shopid,message,username):
    db = create_connection()
    con = db.cursor()
    print('id'+shopid)
    rows=con.execute("insert into comments(contents,username,shopunid) values('%s','%s','%d')" % (message,username,int(shopid.strip())))
    con.close()
    db.close()
    return rows






# -*- coding: utf-8 -*-
import os
from datetime import timedelta

from flask import Flask, render_template, request, session, jsonify, redirect
from models import Shop
from dbapis import *

application = Flask(__name__)

application.config['SECRET_KEY'] = os.urandom(24)
application.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)


@application.route('/booklist')
def page_shoplist():
    if 'loginuser' not in session: return redirect('/login')
    books = get_all_shop()
    if len(books) % 10 != 0:
        pageAll = int(len(books) / 10) + 1
    else:
        pageAll = int(len(books) / 10)
    return render_template('booklist.html', books = books[0:10],prePage=0,nowPage=1,nextPage=2,pageAll=pageAll)

@application.route('/bookdetail/<bookid>')
def page_bookdetail(bookid):

    return jsonify(result=True)


@application.route('/login', methods=['post'])
def page_login_post():
    username = request.form['username']
    password = request.form['password']
    r = login_user(username, password)
    if r:
        session['shopcart']=0;
        session['toprice']=0;
        session['username']=username
        print('sesss:'+ session['username'])
        return redirect('/showshopindex')
    else:
        notice = 'fail to sign in'
        url = 'http://127.0.0.1:5000'
        page = 'login'
        return render_template('loginfail.html', notice=notice, url=url, page=page)

@application.route('/regist', methods=['post'])
def api_regist():
    username = request.form['username']
    password = request.form['password']
    r = regist_user(UserAccount(username, password))
    if r:
        notice = 'create success'
        url = 'http://127.0.0.1:5000'
        page = 'login'
        return render_template('loginfail.html',notice=notice, url=url, page=page)
    else:
        notice = 'fail to regist'
        url = 'http://127.0.0.1:5000/showregist'
        page = 'regist'
        return render_template('loginfail.html',notice=notice, url=url, page=page)

@application.route('/quite')
def user_quite():

    if session['username']:
        session.pop('username')
        notice = 'success to quite'
        url = 'http://127.0.0.1:5000/'
        page = 'login'
        return render_template('success.html', notice=notice, url=url, page=page)

    else:
        notice = 'you are not logined'
        url = 'http://127.0.0.1:5000/'
        page = 'login'
        return render_template('loginfail.html',notice=notice, url=url, page=page)



@application.route('/addcar/<shopid>/<price>', methods=['get'])
def car_add(shopid,price):
    if session['shopcart']:
        arr=[];
        temp=[];

        arr=session['shopcart']
        session['toprice'] = float(session['toprice']) +float(price)
        temp.applicationend(shopid)
        temp.applicationend(price)
        arr.applicationend(temp)
        session['shopcart']=arr;
    else:
        arr=[];
        temp = [];

        temp.applicationend(shopid)
        temp.applicationend(price)
        arr.applicationend(temp)
        session['toprice']=float(price)
        session['shopcart']=arr;


    return redirect('http://127.0.0.1:5000/showshopindex')

@application.route('/shop_search', methods=['post'])
def shop_search():
    keyword = request.form['keyword']
    results=get_result_search(keyword);


    return render_template('search.html', results=results)



@application.route('/dealcomm', methods=['post'])
def comm_deal():
    shopid = request.form['shopid']
    message = request.form['message']
    print('commuser:' + session['username'])
    username=session['username'];



    r = mess_add(shopid,message,username)
    if r:
        return redirect('http://127.0.0.1:5000/shopdetail/'+shopid)


@application.route('/showlistuser')
def show_user():

    users=get_user_db()
    return render_template('listuser.html',u=users)
@application.route('/')
@application.route('/showlogin')
def page_login():

    return render_template('login.html')

@application.route('/showregist')
def page_regist():
    return render_template('regist.html')

@application.route('/savecomm')
def comm_save():
    return render_template('regist.html')

@application.route('/showcar')
def car_show():
    if session['shopcart']:
        cart = session['shopcart']
    else:
        cart=[]

    return render_template('shopcart.html',cart=cart,prices=session['toprice'])

@application.route('/settle')
def settle():

    return render_template('settle.html',prices=session['toprice'])

@application.route('/cardelete/<shopid>', methods=['GET'])
def car_delete(shopid):
    cart=session['shopcart']
    for i in cart:
        if shopid in i:
            session['toprice'] = float(session['toprice']) - float(i[1]);
            del cart[cart.index(i)]
            break;
    session['shopcart']=cart;
    return render_template('shopcart.html',cart=cart,prices=session['toprice'])


@application.route('/showshopindex')
def showshopindex():
    allshop=get_all_shop();

    return render_template('indexshop.html',u=allshop)



@application.route('/shopdetail/<inshopid>', methods=['GET'])
def shopdetail(inshopid):
    Shop=get_Shop_by_id(inshopid);
    Mess=get_all_mess(inshopid);
    print('detail:' +session['username'])

    return render_template('shopdetail.html',shop=Shop,messes=Mess)


if __name__ == '__main__':
    application.run()

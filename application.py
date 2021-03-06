# -*- coding: utf-8 -*-

import sqlite3
import os
import json
from flask import *
import time as time
from random import randint
import pythonRest

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'database/LS.db'),
    DEBUG=True,
    # 生成秘钥
    SECRET_KEY=os.urandom(24),
    USERNAME='admin',
    PASSWORD='default'
))


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    g.db.close()


@app.route('/goodsList')
def goodsList():
    goods = query_db("select * from goods")
    return jsonify({"goods": goods})


@app.route('/baidu_verify_zQsbmS6VJQ.html')
def baidu_verify():
    return render_template("baidu_verify_zQsbmS6VJQ.html")


# 简化sqlite3的查询方式。
def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


@app.route('/commodity')
def commodity():
    result = query_db(
        'select scope,merchant,c_name,imgURL,price,promotion from merchant m left join tariff t on m.m_id = t.m_id  left join commodity c  on  t.c_id=c.c_id where scope=?',
        [u'松江四期'])
    return render_template("testDy.html", result=result)


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    # user = query_db('select * from user where phone = ?', [username], one=True)
    user = query_db('select * from user where phone = ?', [username], one=True)
    if user is None:
        error = u"用户名不存在。"
    else:
        if password != user['passwd']:
            error = u"密码不正确。"
        else:
            # return jsonify({"msg": "YES", "contact": user['phone'], "addr": user['addr'], "name": user['name']})
            return jsonify({"msg": "YES", "contact": user['phone'], "addr": user['school'], "name": user['name'],
                            "u_type": user['u_type']})
    return jsonify({"msg": error})


# 注册。
@app.route('/register', methods=['GET', 'POST'])
def register():
    error_r = None

    if request.method == 'POST':
        # user = query_db('select * from user where name = ?', [request.form['username']], one=True)
        user = query_db('select * from user where name = ?', [request.form['username']], one=True)
        phone = query_db('select * from user where phone = ?', [request.form['contact']], one=True)
        # phone = query_db('select * from user where phone = ?', [request.form['contact']], one=True)
        # isVIP = query_db('select * from user_vip where phone = ?', [request.form['contact']], one=True)
        if user is not None:
            error = "REPEAT"
        elif phone is not None:
            error = "PHONE"
        elif session['key'] != request.form['validation']:
            error = "ERR"
        else:
            # if isVIP is not  None:
            #     g.db.execute('insert into user (name, passwd, phone, school,u_type, time) values (?, ?, ?, ?, ?, ?)',
            #                  [request.form['username'], request.form['password'], request.form['contact'],
            #                   request.form['addr'], u'VIP会员', int(time.time())])
            #     g.db.commit()
            #     error = "YES"
            #
            # else:
            g.db.execute('insert into user (name, passwd, phone, school,u_type, time) values (?, ?, ?, ?, ?, ?)',
                         [request.form['username'], request.form['password'], request.form['contact'],
                          request.form['addr'], u'普通用户', int(time.time())])
            g.db.commit()
            error = "YES"
            # g.db.execute('insert into user (name, passwd, phone, addr, time) values (?, ?, ?, ?, ?)', [request.form['username'], request.form['password'], request.form['contact'], request.form['addr'], int(time.time())])
            # g.db.execute('insert into user (name, passwd, phone, school,u_type, time) values (?, ?, ?, ?, ?, ?)',
            #              [request.form['username'], request.form['password'], request.form['contact'],
            #               request.form['addr'], u'普通用户', int(time.time())])
            # g.db.commit()
            # error = "YES"
    return jsonify({"msg": error})


# 修改密码
@app.route('/modifyPassword', methods=['GET', 'POST'])
def modifyPassword():
    error = None
    if request.method == 'POST':

        phone = query_db('select * from user where phone = ?', [request.form['contact']], one=True)
        # print phone
        if phone is None:
            error = "PHONE"
        elif session['key'] != request.form['validation']:
            error = "ERR"
        else:
            g.db.execute('update user set passwd =?  where phone=?',
                         [request.form['password'], request.form['contact']])
            g.db.commit()
            error = "YES"

    return jsonify({"msg": error})


# 修改密码new
@app.route('/updatePassword', methods=['GET', 'POST'])
def updatePassword():
    error = None
    if request.method == 'POST':

        phone = query_db('select * from user where phone = ?', [request.form['contact']], one=True)
        # print phone
        if phone is None:
            error = "PHONE"
        elif session['key'] != request.form['validation']:
            error = "ERR"
        else:
            g.db.execute('update user set passwd =?  where phone=?',
                         [request.form['password'], request.form['contact']])
            g.db.commit()
            error = "YES"

    return jsonify({"msg": error})


@app.route('/uRegister')
def uRegister():
    return render_template("register.html")


@app.route('/ulogin')
def ulogin():
    return render_template("login.html")


@app.route('/uReset')
def uReset():
    return render_template("resetPassword.html")


@app.route('/uterm')
def uTerm():
    return render_template("term.html")


@app.route('/')
def index():
    if request.cookies.get('dizhi'):

        print
        request.cookies.get('schoolname')
        nameSchool = utilMethod(request.cookies.get('schoolname'))
        resultClothes = query_db(
            'select scope,merchant,c_name,imgURL,price,promotion,disPrice from merchant m left join tariff t on m.m_id = t.m_id  left join commodity c  on  t.c_id=c.c_id where c_type = 0 and scope=?',
            [nameSchool])
        resultShoes = query_db(
            'select scope,merchant,c_name,imgURL,price,promotion,disPrice from merchant m left join tariff t on m.m_id = t.m_id  left join commodity c  on  t.c_id=c.c_id where c_type = 1 and scope=?',
            [nameSchool])
        result = query_db(
            'select scope,merchant,c_name,imgURL,price,promotion,disPrice from merchant m left join tariff t on m.m_id = t.m_id  left join commodity c  on  t.c_id=c.c_id where c_type = 2 and scope=?',
            [nameSchool])
        return render_template("goods.html", result=result, resultClothes=resultClothes, resultShoes=resultShoes)
    else:
        return render_template("index.html")


def utilMethod(schoolName):
    if (schoolName == 'jiaotong'):
        return u'上海交通大学'
    if (schoolName == 'huashida'):
        return u'华东师范大学'
    if (schoolName == 'songjiang1'):
        return u'松江一期'
    if (schoolName == 'songjiang2'):
        return u'松江二期'
    if (schoolName == 'songjiang3'):
        return u'松江三期'
    if (schoolName == 'songjiang4'):
        return u'松江四期'
    if (schoolName == 'songjiang5'):
        return u'松江五期'
    if (schoolName == 'songjiang6'):
        return u'松江六期'
    if (schoolName == 'fudannan'):
        return u'复旦南区'
    if (schoolName == 'fudanbei'):
        return u'复旦北区'
    if (schoolName == 'tongji'):
        return u'同济大学'
    if (schoolName == 'caijingdaxue'):
        return u'上海财经大学'
    if (schoolName == 'jiaodaxuhui'):
        return u'上海交通大学(徐汇)'
    return u''


@app.route('/faq')
def faqPage():
    return render_template("faq.html")


@app.route('/sendKey', methods=['GET', 'POST'])
def sendKeyPage():
    key = randint(10000, 99999)
    session['key'] = str(key)
    session['number'] = request.form.get("contact")
    return jsonify({"msg": pythonRest.sendKey(key, request.form.get("contact"))})


@app.route('/checkPhone', methods=['GET', 'POST'])
def checkPhonePage():
    if request.form.get('key') == "6666":
        cart = query_db('select * from cart where contact = ? order by ID desc', [request.form.get('contact')])
        return jsonify({"msg": "OK", "cart": cart})
    if session.get('number') and session.get('key'):
        if session['number'] == request.form.get("contact") and session['key'] == request.form.get("key"):
            cart = query_db('select * from cart where contact = ? order by ID desc', [session['number']])
            return jsonify({"msg": "OK", "cart": cart})
    return jsonify({"msg": "Wrong"})


@app.route('/queryOrders', methods=['GET', 'POST'])
def queryOrders():
    cart = query_db('select * from cart where phone = ? order by ID desc', [request.form.get('phone')])

    return jsonify({"msg": "OK", "cart": cart})


@app.route('/queryMembership', methods=['GET', 'POST'])
def queryMembership():
    member = query_db('select * from membership where level_name="VIP会员"')
    return jsonify({"member": member})


@app.route('/back/orders/login', methods=['GET', 'POST'])
def backLogin():
    if request.method == 'POST':
        if request.form['usernm'] == "xjcsjtu" and request.form['passwd'] == "getwash.123":
            session['Admin'] = "1"
            session['xuexiao'] = "total"
            return redirect(url_for('getBackOrder'))
        if request.form['usernm'] == "SJTU" and request.form['passwd'] == "jiaodazhou":
            session['Admin'] = "0"
            session['xuexiao'] = "SJTU"
            return redirect(url_for('getBackOrder'))
        if request.form['usernm'] == "ECNU" and request.form['passwd'] == "huashizhou":
            session['Admin'] = "0"
            session['xuexiao'] = "ECNU"
            return redirect(url_for('getBackOrder'))

        if request.form['usernm'] == "HSSW" and request.form['passwd'] == "HSSW":
            session['Admin'] = "0"
            session['xuexiao'] = "HSSW"
            return redirect(url_for('getBackOrder'))
        if request.form['usernm'] == "SJUCC" and request.form['passwd'] == "SJUCC":
            session['Admin'] = "0"
            session['xuexiao'] = "SJUCC"
            return redirect(url_for('getBackOrder'))
        if request.form['usernm'] == "SJHSLJ" and request.form['passwd'] == "SJHSLJ":
            session['Admin'] = "0"
            session['xuexiao'] = "SJHSLJ"
            return redirect(url_for('getBackOrder'))
        if request.form['usernm'] == "SJSW" and request.form['passwd'] == "SJSW":
            session['Admin'] = "0"
            session['xuexiao'] = "SJSW"
            return redirect(url_for('getBackOrder'))
        if request.form['usernm'] == "FDBHSLJ" and request.form['passwd'] == "FDBHSLJ":
            session['Admin'] = "0"
            session['xuexiao'] = "FDBHSLJ"
            return redirect(url_for('getBackOrder'))
        if request.form['usernm'] == "FDNJLYL" and request.form['passwd'] == "FDNJLYL":
            session['Admin'] = "0"
            session['xuexiao'] = "FDNJLYL"
            return redirect(url_for('getBackOrder'))
        if request.form['usernm'] == "SCXW" and request.form['passwd'] == "SCXW":
            session['Admin'] = "0"
            session['xuexiao'] = "SCXW"
            return redirect(url_for('getBackOrder'))
        if request.form['usernm'] == "TJJF" and request.form['passwd'] == "TJJF":
            session['Admin'] = "0"
            session['xuexiao'] = "TJJF"
            return redirect(url_for('getBackOrder'))
        if request.form['usernm'] == "SJXH" and request.form['passwd'] == "SJXH":
            session['Admin'] = "0"
            session['xuexiao'] = "SJXH"
            return redirect(url_for('getBackOrder'))
        return redirect(url_for('backLogin'))
    else:
        return render_template("back_login.html")


# 订单表，一星期之内。
@app.route('/back/orders')
def getBackOrder():
    if session.get('Admin'):
        if session['xuexiao'] == "total":
            # orders = query_db('select * from cart where time>? order by ID desc', [int(time.time())-604800])
            orders = query_db(
                'select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone where c.time>? order by ID desc',
                [int(time.time()) - 604800])
            return render_template("back.html", orders=orders, auth=session['Admin'])
        if session['xuexiao'] == "SJTU":
            # orders = query_db('select * from cart where substr(deliver, 0, 7)=? and id not in(select id from cart where substr(deliver, 0, 11)=?)  and time>? order by ID desc', [u'上海交通大学',u'上海交通大学(徐汇)', int(time.time())-604800])
            orders = query_db(
                'select  c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone where substr(deliver, 0, 7)=? and c.id not in(select id from cart where substr(deliver, 0, 11)=?)  and c.time>? order by ID desc',
                [u'上海交通大学', u'上海交通大学(徐汇)', int(time.time()) - 604800])
            return render_template("back.html", orders=orders, auth=session['Admin'])
        if session['xuexiao'] == "ECNU":
            # orders = query_db('select * from cart where substr(deliver, 0, 7)=? and time>? order by ID desc', [u'华东师范大学', int(time.time())-604800])
            orders = query_db(
                'select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone where substr(deliver, 0, 7)=? and c.time>? order by ID desc',
                [u'华东师范大学', int(time.time()) - 604800])
            return render_template("back.html", orders=orders, auth=session['Admin'])

        if session['xuexiao'] == "TJJF":
            # orders = query_db('select * from cart where substr(deliver, 0, 5)=? and time>? order by ID desc', [u'同济大学', int(time.time())-604800])
            orders = query_db(
                'select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone where substr(deliver, 0, 5)=? and c.time>? order by ID desc',
                [u'同济大学', int(time.time()) - 604800])
            return render_template("back.html", orders=orders, auth=session['Admin'])
        if session['xuexiao'] == "HSSW":
            # orders = query_db('select * from cart where substr(deliver, 0, 7)=? and time>? order by ID desc', [u'华东师范大学', int(time.time())-604800])
            orders = query_db(
                'select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone where substr(deliver, 0, 7)=? and c.time>? order by ID desc',
                [u'华东师范大学', int(time.time()) - 604800])
            return render_template("back.html", orders=orders, auth=session['Admin'])
        if session['xuexiao'] == "SJUCC":
            # orders = query_db('select * from cart where substr(deliver, 0, 5) in ("松江五期","松江六期") and time>? order by ID desc', [ int(time.time())-604800])
            orders = query_db(
                'select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone where substr(deliver, 0, 5) in ("松江五期","松江六期") order by ID desc')
            return render_template("back.html", orders=orders, auth=session['Admin'])

        if session['xuexiao'] == "SJHSLJ":
            # orders = query_db('select * from cart where substr(deliver, 0, 5)=? and time>? order by ID desc', [u'松江四期', int(time.time())-604800])
            orders = query_db(
                'select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone where substr(deliver, 0, 5)=? and c.time>? order by ID desc',
                [u'松江四期', int(time.time()) - 604800])
            return render_template("back.html", orders=orders, auth=session['Admin'])

        if session['xuexiao'] == "SJSW":
            # orders = query_db('select * from cart where substr(deliver, 0, 5) in("松江一期","松江二期","松江三期") and time>? order by ID desc', [ int(time.time())-604800])
            orders = query_db(
                'select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone where substr(deliver, 0, 5) in("松江一期","松江二期","松江三期") and c.time>? order by ID desc',
                [int(time.time()) - 604800])
            return render_template("back.html", orders=orders, auth=session['Admin'])
        if session['xuexiao'] == "FDBHSLJ":
            # orders = query_db('select * from cart where substr(deliver, 0, 5)=? and time>? order by ID desc', [u'复旦北区', int(time.time())-604800])
            orders = query_db(
                'select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone where substr(deliver, 0, 5)=? and c.time>? order by ID desc',
                [u'复旦北区', int(time.time()) - 604800])
            return render_template("back.html", orders=orders, auth=session['Admin'])
        if session['xuexiao'] == "FDNJLYL":
            # orders = query_db('select * from cart where substr(deliver, 0, 5)=? and time>? order by ID desc', [u'复旦大学', int(time.time())-604800])
            orders = query_db(
                'select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone where substr(deliver, 0, 5)=? and c.time>? order by ID desc',
                [u'复旦大学', int(time.time()) - 604800])
            return render_template("back.html", orders=orders, auth=session['Admin'])
        if session['xuexiao'] == "SCXW":
            # orders = query_db('select * from cart where substr(deliver, 0, 7)=? and time>? order by ID desc', [u'上海财经大学', int(time.time())-604800])
            orders = query_db(
                'select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone where substr(deliver, 0, 7)=? and c.time>? order by ID desc',
                [u'上海财经大学', int(time.time()) - 604800])
            return render_template("back.html", orders=orders, auth=session['Admin'])
        if session['xuexiao'] == "SJXH":
            # orders = query_db('select * from cart where substr(deliver, 0, 11)=? and time>? order by ID desc', [u'上海交通大学(徐汇)', int(time.time())-604800])
            orders = query_db(
                'select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone where substr(deliver, 0, 11)=? and c.time>? order by ID desc',
                [u'上海交通大学(徐汇)', int(time.time()) - 604800])
            return render_template("back.html", orders=orders, auth=session['Admin'])

    else:
        return redirect(url_for('backLogin'))


# 订单表，全部。
@app.route('/back/orders/all')
def getBackOrder_ALL():
    if session.get('Admin'):
        if session['xuexiao'] == "total":
            # orders = query_db('select * from cart order by ID desc')
            orders = query_db(
                'select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone order by ID desc')
            return render_template("back.html", orders=orders, auth=session['Admin'], all=1)
        if session['xuexiao'] == "SJTU":
            # orders = query_db('select * from cart where substr(deliver, 0, 7)=? and id not in(select id from cart where substr(deliver, 0, 11)=?)  order by ID desc', [u'上海交通大学',u'上海交通大学(徐汇)'])
            orders = query_db(
                'select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone where substr(deliver, 0, 7)=? and c.id not in(select id from cart where substr(deliver, 0, 11)=?)  order by ID desc',
                [u'上海交通大学', u'上海交通大学(徐汇)'])
            return render_template("back.html", orders=orders, auth=session['Admin'], all=1)
        if session['xuexiao'] == "ECNU":
            # orders = query_db('select * from cart where substr(deliver, 0, 7)=? order by ID desc', [u'华东师范大学'])
            orders = query_db(
                'select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone where substr(deliver, 0, 7)=? order by ID desc',
                [u'华东师范大学'])
            return render_template("back.html", orders=orders, auth=session['Admin'], all=1)

        if session['xuexiao'] == "TJJF":
            # orders = query_db('select * from cart where substr(deliver, 0, 5)=? order by ID desc', [u'同济大学'])
            orders = query_db(
                'select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone where substr(deliver, 0, 5)=? order by ID desc',
                [u'同济大学'])
            return render_template("back.html", orders=orders, auth=session['Admin'], all=1)
        if session['xuexiao'] == "HSSW":
            # orders = query_db('select * from cart where substr(deliver, 0, 7)=? order by ID desc', [u'同济大学北区'])
            orders = query_db(
                'select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone where substr(deliver, 0, 7)=? order by ID desc',
                [u'同济大学北区'])
            return render_template("back.html", orders=orders, auth=session['Admin'], all=1)
        if session['xuexiao'] == "SJUCC":
            # orders = query_db('select * from cart where substr(deliver, 0, 7)=? order by ID desc', [u'同济大学北区'])
            orders = query_db(
                'select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone where substr(deliver, 0, 5) in ("松江五期","松江六期")  order by ID desc')
            return render_template("back.html", orders=orders, auth=session['Admin'], all=1)
        if session['xuexiao'] == "SJHSLJ":
            # orders = query_db('select * from cart where substr(deliver, 0, 7)=? order by ID desc', [u'同济大学北区'])
            orders = query_db(
                'select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone where substr(deliver, 0, 5) in ("松江四期") order by ID desc')
            return render_template("back.html", orders=orders, auth=session['Admin'], all=1)
        if session['xuexiao'] == "SJSW":
            # orders = query_db('select * from cart where substr(deliver, 0, 7)=? order by ID desc', [u'同济大学北区'])
            orders = query_db(
                'select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone where substr(deliver, 0, 5) in("松江一期","松江二期","松江三期") order by ID desc')
            return render_template("back.html", orders=orders, auth=session['Admin'], all=1)
        if session['xuexiao'] == "FDBHSLJ":
            # orders = query_db('select * from cart where substr(deliver, 0, 5)=? order by ID desc', [u'复旦北区'])
            orders = query_db(
                'select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone where substr(deliver, 0, 5)=? order by ID desc',
                [u'复旦北区'])
            return render_template("back.html", orders=orders, auth=session['Admin'], all=1)
        if session['xuexiao'] == "FDNJLYL":
            # orders = query_db('select * from cart where substr(deliver, 0, 5)=? order by ID desc', [u'复旦大学'])
            orders = query_db(
                'select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone where substr(deliver, 0, 5)=? order by ID desc',
                [u'复旦大学'])
            return render_template("back.html", orders=orders, auth=session['Admin'], all=1)
        if session['xuexiao'] == "SCXW":
            # orders = query_db('select * from cart where substr(deliver, 0, 7)=? order by ID desc', [u'上海财经大学'])
            orders = query_db(
                'select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone where substr(deliver, 0, 7)=? order by ID desc',
                [u'上海财经大学'])
            return render_template("back.html", orders=orders, auth=session['Admin'], all=1)
        if session['xuexiao'] == "SJUCC":
            # orders = query_db('select * from cart where substr(deliver, 0, 7)=? order by ID desc', [u'上海财经大学'])
            orders = query_db(
                'select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone where substr(deliver, 0, 5) in("松江五期","松江六期")  order by ID desc')
            return render_template("back.html", orders=orders, auth=session['Admin'], all=1)

        if session['xuexiao'] == "SJXH":
            # orders = query_db('select * from cart where substr(deliver, 0, 11)=? order by ID desc', [u'上海交通大学(徐汇)'])
            orders = query_db(
                'select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment, vipPrice, oldPrice from cart c left join user u on c.phone=u.phone where substr(deliver, 0, 11)=? order by ID desc',
                [u'上海交通大学(徐汇)'])
            return render_template("back.html", orders=orders, auth=session['Admin'], all=1)
    else:
        return redirect(url_for('backLogin'))


# 反馈表。
@app.route('/back/advices')
def getBackAdvice():
    if session.get('Admin'):
        advices = query_db('select * from advice order by ID desc')
        return render_template("advice.html", advices=advices)
    else:
        return redirect(url_for('backLogin'))


@app.route('/back/orders/ContactSort')
def ContactSort():
    orders = query_db('select * from cart order by contact')
    return render_template("back.html", orders=orders)


@app.route('/back/orders/AdSort')
def AddrSort():
    orders = query_db('select * from cart order by deliver')
    return render_template("back.html", orders=orders)


@app.route('/back/orders/TimeSort')
def TimeSort():
    orders = query_db('select * from cart order by dtime')
    return render_template("back.html", orders=orders)


@app.route('/back/orders/update', methods=['GET', 'POST'])
def updateOrder():
    state = request.form.get('state')
    pid = request.form.get('id')
    # g.db.execute('update cart set state=? where id=?', [state, pid])
    g.db.execute('update cart set state=? where id=?', [state, pid])
    g.db.commit()
    return jsonify({"msg": "OK"})


@app.route('/back/orders/addBeizhu', methods=['GET', 'POST'])
def addBeizhu():
    beizhu = request.form.get('beizhu')
    pid = request.form.get('id')
    # g.db.execute('update cart set comment=? where id=?', [beizhu, pid])
    g.db.execute('update cart set comment=? where id=?', [beizhu, pid])
    g.db.commit()
    return jsonify({"msg": "OK"})


@app.route('/back/orders/checkUpdate', methods=['GET', 'POST'])
def checkUpdate():
    if session.get('Admin'):
        t = request.form.get('time')
        if session['xuexiao'] == "total":
            # orders = query_db('select * from cart where time>? order by ID desc',[int(time.time())-int(t)])
            orders = query_db('select * from cart where time>? order by ID desc', [int(time.time()) - int(t)])
        if session['xuexiao'] == "SJTU":
            orders = query_db(
                'select * from cart where substr(deliver, 0, 7)=? and id not in(select id from cart where substr(deliver, 0, 11)=?) and time>? order by ID desc',
                [u'上海交通大学', u'上海交通大学(徐汇)', int(time.time()) - int(t)])
            # orders = query_db('select * from cart where substr(deliver, 0, 7)=? and id not in(select id from cart where substr(deliver, 0, 11)=?) and time>? order by ID desc', [u'上海交通大学',u'上海交通大学(徐汇)',int(time.time())-int(t)])
        if session['xuexiao'] == "ECNU":
            # orders = query_db('select * from cart where substr(deliver, 0, 7)=? and time>? order by ID desc', [u'华东师范大学',int(time.time())-int(t)])
            orders = query_db('select * from cart where substr(deliver, 0, 7)=? and time>? order by ID desc',
                              [u'华东师范大学', int(time.time()) - int(t)])
        if session['xuexiao'] == "TJJF":
            # orders = query_db('select * from cart where substr(deliver, 0, 5)=? and time>? order by ID desc', [u'同济大学 ',int(time.time())-int(t)])
            orders = query_db('select * from cart where substr(deliver, 0, 5)=? and time>? order by ID desc',
                              [u'同济大学 ', int(time.time()) - int(t)])
        if session['xuexiao'] == "HSSW":
            # orders = query_db('select * from cart where substr(deliver, 0, 7)=? and time>? order by ID desc', [u'同济大学',int(time.time())-int(t)])
            orders = query_db('select * from cart where substr(deliver, 0, 7)=? and time>? order by ID desc',
                              [u'同济大学', int(time.time()) - int(t)])
        if session['xuexiao'] == "SJUCC":
            # orders = query_db('select * from cart where substr(deliver, 0, 7)=? and time>? order by ID desc', [u'同济大学',int(time.time())-int(t)])
            orders = query_db('select * from cart where substr(deliver, 0, 7)=? and time>? order by ID desc',
                              [u'同济大学', int(time.time()) - int(t)])
        if session['xuexiao'] == "SJHSLJ":
            # orders = query_db('select * from cart where substr(deliver, 0, 7)=? and time>? order by ID desc', [u'同济大学',int(time.time())-int(t)])
            orders = query_db('select * from cart where substr(deliver, 0, 7)=? and time>? order by ID desc',
                              [u'同济大学', int(time.time()) - int(t)])
        if session['xuexiao'] == "SJSW":
            # orders = query_db('select * from cart where substr(deliver, 0, 5)=? and time>? order by ID desc', [u'同济大学',int(time.time())-int(t)])
            orders = query_db('select * from cart where substr(deliver, 0, 5)=? and time>? order by ID desc',
                              [u'同济大学', int(time.time()) - int(t)])
        if session['xuexiao'] == "FDBHSLJ":
            # orders = query_db('select * from cart where substr(deliver, 0, 5)=? and time>? order by ID desc', [u'复旦北区',int(time.time())-int(t)])
            orders = query_db('select * from cart where substr(deliver, 0, 5)=? and time>? order by ID desc',
                              [u'复旦北区', int(time.time()) - int(t)])
        if session['xuexiao'] == "FDNJLYL":
            # orders = query_db('select * from cart where substr(deliver, 0, 5)=? and time>? order by ID desc', [u'复旦大学',int(time.time())-int(t)])
            orders = query_db('select * from cart where substr(deliver, 0, 5)=? and time>? order by ID desc',
                              [u'复旦大学', int(time.time()) - int(t)])
        if session['xuexiao'] == "SCXW":
            # orders = query_db('select * from cart where substr(deliver, 0, 7)=? and time>? order by ID desc', [u'上海财经大学',int(time.time())-int(t)])
            orders = query_db('select * from cart where substr(deliver, 0, 7)=? and time>? order by ID desc',
                              [u'上海财经大学', int(time.time()) - int(t)])
        if session['xuexiao'] == "SJXH":
            # orders = query_db('select * from cart where substr(deliver, 0, 11)=? and time>? order by ID desc', [u'上海交通大学(徐汇)', int(time.time()) - int(t)])
            orders = query_db('select * from cart where substr(deliver, 0, 11)=? and time>? order by ID desc',
                              [u'上海交通大学(徐汇)', int(time.time()) - int(t)])

        return jsonify({"order": orders})
    else:
        return redirect(url_for('backLogin'))


@app.route('/back/orders/remove', methods=['GET', 'POST'])
def removeOrder():
    pid = request.form.get('id')
    # g.db.execute('delete from cart where id=?', [pid])
    g.db.execute('delete from cart where id=?', [pid])
    g.db.commit()
    return jsonify({"msg": "OK"})


@app.route('/advice', methods=['GET', 'POST'])
def advice():
    if request.form.get('contact'):
        g.db.execute('insert into advice (content, contact, time) values (?, ?, ?)',
                     [request.form.get('advice'), request.form.get('contact'), int(time.time())])
    else:
        g.db.execute('insert into advice (content, time) values (?, ?)', [request.form.get('advice'), int(time.time())])
    g.db.commit()
    return jsonify({"msg": "OK"})


@app.route('/toudi', methods=['GET', 'POST'])
def toudi():
    dizhi = request.form.get('dizhi')
    shouji = request.form.get('shouji')
    shijian = request.form.get('shijian')
    content = request.form.get('content')
    liuyan = request.form.get('note')
    scope = request.form.get('scope')
    vip_price = request.form.get('vip_price')
    old_price = request.form.get('old_price')

    # g.db.execute('insert into cart (contact, list, note, deliver, time, pickup, dtime, ptime) values (?, ?, ?, ?, ?, ?, ?, ?)',
    g.db.execute(
        'insert into cart (phone, list, note, deliver, time, pickup, dtime, ptime,scope,vipPrice,oldPrice) values (?, ?, ?, ?, ?, ?, ?, ?,?,?,?)',
        [shouji, content, liuyan, dizhi, int(time.time()), dizhi, shijian, shijian, scope, vip_price, old_price])
    g.db.commit()
    return jsonify({"msg": "OK"})


@app.route('/dizhi', methods=['GET', 'POST'])
def dizhi():
    session['addr'] = request.form.get('dizhi');
    return jsonify({"msg": "OK"})


@app.route('/deldizhi', methods=['GET', 'POST'])
def deldizhi():
    session['addr'] = None;
    return jsonify({"msg": "OK"})


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    post = request.get_json()
    username = post.get('username')
    password = post.get('password')
    phonenum = post.get('phonenum')
    address = post.get('address')
    user = query_db('select * from user where name = ?', [username], one=True)
    if user is not None:
        error = u"用户名重复。"
        return jsonify({"msg": "NO"})
    else:
        g.db.execute('insert into user (name, passwd, phone, addr, time) values (?, ?, ?, ?, ?)',
                     [username, password, phonenum, address, time.time()])
        g.db.commit()
        return jsonify({"msg": "YES"})


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    post = request.get_json()
    contact = post.get('contact')
    content = post.get('content')
    g.db.execute('insert into advice (contact, content, time) values (?, ?, ?)', [contact, content, time.time()])
    g.db.commit()
    return jsonify({"msg": "YES"})


@app.route('/roadPlan/getNews', methods=['GET', 'POST'])
def getNews():
    a = {"details": [
        {"title": "我是标题", "content": "first", "img": "http://7xitj5.com1.z0.glb.clouddn.com/static/img/logo_new.png",
         "source": "新浪微博", "time": "2015.5.27 12:00", "link": "ahahahahah"},
        {"title": "我是标题", "content": "first", "img": "http://7xitj5.com1.z0.glb.clouddn.com/static/img/logo_new.png",
         "source": "新浪微博", "time": "2015.5.27 12:00", "link": "ahahahahah"},
        {"title": "我是标题", "content": "first", "img": "http://7xitj5.com1.z0.glb.clouddn.com/static/img/logo_new.png",
         "source": "新浪微博", "time": "2015.5.27 12:00", "link": "ahahahahah"}]}
    return jsonify(a)


@app.route('/refresh')
def refresh():
    if session.get('logged_in'):
        user = query_db('select noticenum, notification from user where username = ?', [session['username']], one=True)
        if user['notification']:
            notifications = user['notification'].split('###')
        else:
            notifications = ['空', ''];
        js = {"num": user["noticenum"], "value": notifications[len(notifications) - 2]}
        return jsonify(js)
    else:
        return redirect(url_for('welcome'));


# 退出登录。
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


# 投条。
@app.route('/post', methods=['GET', 'POST'])
def postOrder():
    if session.get('logged_in'):
        user = query_db('select * from user where username = ?', [session['username']], one=True)
        if user['notification']:
            user['notification'] = user['notification'].split('###')
        if request.method == 'POST':
            nicecard = query_db('select nicecard from user where username = ?', [session['username']], one=True)
            nicecard_new = nicecard['nicecard'] - int(request.form['money'])
            if request.form.get('is_anonymity'):
                g.db.execute(
                    'insert into item (username, content, is_anonymity, position, time, nicecard) values (?, ?, ?, ?, ?, ?)',
                    [session['username'], request.form['content'].strip(' '), request.form['is_anonymity'],
                     request.form['position'], request.form['time'], int(request.form['money'])])
            else:
                g.db.execute('insert into item (username, content, position, time, nicecard) values (?, ?, ?, ?, ?)',
                             [session['username'], request.form['content'].strip(' '), request.form['position'],
                              request.form['time'], int(request.form['money'])])
            g.db.execute('update user set nicecard = ? where username = ?', [nicecard_new, session['username']])
            g.db.commit()
            return render_template('postOrder.html', user=user)
        return render_template('postOrder.html', user=user)
    else:
        return redirect(url_for('welcome'))


# 接单表。
@app.route('/get')
def getOrder():
    if session.get('logged_in'):
        error = None
        if request.args.get('error'):
            error = request.args.get('error')
        success = None
        if request.args.get('success'):
            success = request.args.get('success')
        user = query_db('select * from user where username = ?', [session['username']], one=True)
        if user['notification']:
            user['notification'] = user['notification'].split('###')
        orders = query_db('select * from item')
        orders.reverse()
        local_time_array = time.localtime()
        for order in orders:
            get_time_array = time.strptime(order['time'], u"%Y年%m月%d日%H时%M分")
            if get_time_array.tm_year - local_time_array.tm_year == 0:
                if get_time_array.tm_mon - local_time_array.tm_mon == 0:
                    if get_time_array.tm_mday - local_time_array.tm_mday == 0:
                        if get_time_array.tm_hour - local_time_array.tm_hour == 0:
                            order['time'] = str(local_time_array.tm_min - get_time_array.tm_min) + u"分钟前"
                        else:
                            order['time'] = str(local_time_array.tm_hour - get_time_array.tm_hour) + u"小时前"
                    else:
                        order['time'] = str(local_time_array.tm_mday - get_time_array.tm_mday) + u"天前"
                else:
                    order['time'] = str(local_time_array.tm_mon - get_time_array.tm_mon) + u"月前"
            else:
                order['time'] = str(local_time_array.tm_year - get_time_array.tm_year) + u"年前"
        return render_template('getOrder.html', orders=orders, user=user, error=error, success=success)
    else:
        return redirect(url_for('welcome'))


# 接单表。
@app.route('/androidget')
def getandroidOrder():
    orders = query_db('select * from item')
    orders.reverse()
    local_time_array = time.localtime()
    for order in orders:
        get_time_array = time.strptime(order['time'], u"%Y年%m月%d日%H时%M分")
        if get_time_array.tm_year - local_time_array.tm_year == 0:
            if get_time_array.tm_mon - local_time_array.tm_mon == 0:
                if get_time_array.tm_mday - local_time_array.tm_mday == 0:
                    if get_time_array.tm_hour - local_time_array.tm_hour == 0:
                        order['time'] = str(local_time_array.tm_min - get_time_array.tm_min) + u"分钟前"
                    else:
                        order['time'] = str(local_time_array.tm_hour - get_time_array.tm_hour) + u"小时前"
                else:
                    order['time'] = str(local_time_array.tm_mday - get_time_array.tm_mday) + u"天前"
            else:
                order['time'] = str(local_time_array.tm_mon - get_time_array.tm_mon) + u"月前"
        else:
            order['time'] = str(local_time_array.tm_year - get_time_array.tm_year) + u"年前"
    tmp = str(orders)
    return tmp.replace("u\'", "\'")


# 交易。
@app.route('/deal/<int:post_id>', methods=['GET', 'POST'])
def dealOrder(post_id):
    error = None
    success = None
    if session.get('logged_in'):
        post_state = query_db('select state from item where id = ?', [post_id], one=True)
        if post_state['state'] == 1:
            error = u"这个单子已经处于交易中！"
            return redirect(url_for('getOrder', error=error))
        elif post_state['state'] == 2:
            error = u"这个单子已经完成了！"
            return redirect(url_for('getOrder', error=error))
        elif post_state['state'] == 0:
            username = query_db('select username from item where id = ?', [post_id], one=True)
            if username['username'] == session['username']:
                error = u"你不能接受自己的投条！"
                return redirect(url_for('getOrder', error=error))
            g.db.execute('update item set state = 1, dealername = ? where id = ?', [session['username'], post_id])
            post_letter = session['username'] + u"向你ID为" + str(post_id) + u"的订单发起交易。###"
            post_letter_old = query_db('select notification from user where username = ?', [username['username']],
                                       one=True)
            noticenum = query_db('select noticenum from user where username = ?', [username['username']], one=True)
            if post_letter_old['notification']:
                g.db.execute('update user set notification = ?, noticenum = ? where username = ?',
                             [post_letter_old['notification'] + post_letter, noticenum['noticenum'] + 1,
                              username['username']])
            else:
                g.db.execute('update user set notification = ?, noticenum = ? where username = ?',
                             [post_letter, noticenum['noticenum'] + 1, username['username']])
            g.db.commit()
        return redirect(url_for('getOrder', success=u"操作成功~"))
    else:
        return redirect(url_for('welcome'))


# 私信。
@app.route('/letter/<int:post_id>', methods=['GET', 'POST'])
def letter(post_id):
    success = None
    error = None
    if session.get('logged_in'):
        username = query_db('select username from item where id = ?', [post_id], one=True)
        if username['username'] == session['username']:
            error = u"给自己私信是没有意义的哟！"
            return redirect(url_for('getOrder', error=error))
        else:
            if request.method == 'POST':
                post_letter = session['username'] + u"向你发送消息：" + request.form['content'] + u"###"
                noticenum = query_db('select noticenum from user where username = ?', [username['username']], one=True)
                post_letter_old = query_db('select notification from user where username = ?', [username['username']],
                                           one=True)
                if post_letter_old['notification']:
                    g.db.execute('update user set notification = ?, noticenum = ? where username = ?',
                                 [post_letter_old['notification'] + post_letter, noticenum['noticenum'] + 1,
                                  username['username']])
                else:
                    g.db.execute('update user set notification = ?, noticenum = ? where username = ?',
                                 [post_letter, noticenum['noticenum'] + 1, username['username']])
                g.db.commit()
                return redirect(url_for('getOrder', success=u"发送成功~"))
    else:
        return redirect(url_for('welcome'))


# 私信 - 发给接单人。
@app.route('/letter_deal/<int:post_id>', methods=['GET', 'POST'])
def letter_deal(post_id):
    success = None
    error = None
    if session.get('logged_in'):
        username = query_db('select dealername from item where id = ?', [post_id], one=True)
        if request.method == 'POST':
            post_letter = session['username'] + u"向你发送消息：" + request.form['content'] + u"###"
            noticenum = query_db('select noticenum from user where username = ?', [username['dealername']], one=True)
            post_letter_old = query_db('select notification from user where username = ?', [username['dealername']],
                                       one=True)
            if post_letter_old['notification']:
                g.db.execute('update user set notification = ?, noticenum = ? where username = ?',
                             [post_letter_old['notification'] + post_letter, noticenum['noticenum'] + 1,
                              username['dealername']])
            else:
                g.db.execute('update user set notification = ?, noticenum = ? where username = ?',
                             [post_letter, noticenum['noticenum'] + 1, username['dealername']])
            g.db.commit()
            return redirect(url_for('getOrder', success=u"发送成功~"))
    else:
        return redirect(url_for('welcome'))


# 活动页面。
@app.route('/event')
def eventActivity():
    if session.get('logged_in'):
        error = None
        if request.args.get('error'):
            error = request.args.get('error')
        success = None
        if request.args.get('success'):
            success = request.args.get('success')
        user = query_db('select * from user where username = ?', [session['username']], one=True)
        if user['notification']:
            user['notification'] = user['notification'].split('###')
        return render_template('eventActivity.html', user=user, error=error, success=success)
    else:
        return redirect(url_for('welcome'))


# 抽奖。
@app.route('/sign')
def signActivity():
    if session.get('logged_in'):
        local_time_array = time.localtime()
        get_time = query_db('select time from user where username = ?', [session['username']], one=True)
        if get_time['time']:
            get_time_array = time.strptime(get_time['time'], u"%Y年%m月%d日")
            if get_time_array.tm_year - local_time_array.tm_year == 0:
                if get_time_array.tm_mon - local_time_array.tm_mon == 0:
                    if get_time_array.tm_mday - local_time_array.tm_mday == 0:
                        error = u"您已经签到过了！"
                        return redirect(url_for('eventActivity', error=error))
                    else:
                        k = randint(-1, 5)
                        nicecard = query_db('select nicecard from user where username = ?', [session['username']],
                                            one=True)
                        g.db.execute('update user set nicecard = ?, time = ? where username = ?',
                                     [nicecard['nicecard'] + k, (
                                         str(local_time_array.tm_year) + u'年' + str(
                                             local_time_array.tm_mon) + u'月' + str(
                                             local_time_array.tm_mday) + u'日'), session['username']])
                        g.db.commit()
                        return redirect(url_for('eventActivity', success=u"您获得奖励：好人卡" + str(k) + u"张！"))
        else:
            k = randint(-1, 5)
            nicecard = query_db('select nicecard from user where username = ?', [session['username']], one=True)
            g.db.execute('update user set nicecard = ?, time = ? where username = ?', [nicecard['nicecard'] + k, (
                str(local_time_array.tm_year) + u'年' + str(local_time_array.tm_mon) + u'月' + str(
                    local_time_array.tm_mday) + u'日'), session['username']])
            g.db.commit()
            return redirect(url_for('eventActivity', success=u"您获得奖励：好人卡" + str(k) + u"张！"))
    return redirect(url_for('welcome'))


# 完成交易。
@app.route('/finish/<int:order_id>/<int:level>', methods=['GET', 'POST'])
def finishOrder(order_id, level):
    if session.get('logged_in'):
        user = query_db('select * from user where username = ?', [session['username']], one=True)
        if user['notification']:
            user['notification'] = user['notification'].split('###')

        dealername = query_db('select dealername, nicecard from item where id = ?', [order_id], one=True);
        username = dealername['dealername']
        if level == 1:
            post_letter = session['username'] + u"完成了交易，给了你好评~\(≧▽≦)/~，单号为" + str(order_id) + u"。###"
        elif level == 2:
            post_letter = session['username'] + u"完成了交易，给了你中评:），单号为" + str(order_id) + u"。###"
        else:
            post_letter = session['username'] + u"完成了交易，给了你差评%>_<%，单号为" + str(order_id) + u"。###"
        noticenum = query_db('select noticenum from user where username = ?', [username], one=True)
        post_letter_old = query_db('select notification from user where username = ?', [username], one=True)
        if post_letter_old['notification']:
            g.db.execute('update user set notification = ?, noticenum = ? where username = ?',
                         [post_letter_old['notification'] + post_letter, noticenum['noticenum'] + 1, username])
        else:
            g.db.execute('update user set notification = ?, noticenum = ? where username = ?',
                         [post_letter, noticenum['noticenum'] + 1, username])
        honor_old = query_db('select honor, nicecard from user where username = ?', [username], one=True)
        if level == 1:
            honor_old['honor'] = honor_old['honor'] * 1.05
        elif level == 2:
            honor_old['honor'] = honor_old['honor'] * 1
        else:
            honor_old['honor'] = honor_old['honor'] * 0.95
        g.db.execute('update user set honor = ?, nicecard = ? where username = ?',
                     [honor_old['honor'], dealername['nicecard'] + honor_old['nicecard'], username])
        g.db.execute('update item set state = ? where id = ?', [2, order_id]);

        g.db.commit();
        return redirect(url_for('welcome'))
    else:
        return redirect(url_for('welcome'))


# 个人设置页面。
@app.route('/setting')
def personalSetting():
    if session.get('logged_in'):
        user = query_db('select * from user where username = ?', [session['username']], one=True)
        if user['notification']:
            user['notification'] = user['notification'].split('###')
        return render_template('personalSetting.html', user=user)
    else:
        return redirect(url_for('welcome'))


# 主页页面。
@app.route('/home')
def homePage():
    if session.get('logged_in'):
        user = query_db('select * from user where username = ?', [session['username']], one=True)
        if user['notification']:
            user['notification'] = user['notification'].split('###')
        post_orders = query_db('select * from item where username = ?', [session['username']])
        get_orders = query_db('select * from item where dealername = ?', [session['username']])
        deal_orders = query_db('select * from item where username = ? and state = 1', [session['username']])
        post_orders.reverse();
        get_orders.reverse();
        deal_orders.reverse();
        local_time_array = time.localtime()
        for order in post_orders:
            post_time_array = time.strptime(order['time'], u"%Y年%m月%d日%H时%M分")
            if post_time_array.tm_year - local_time_array.tm_year == 0:
                if post_time_array.tm_mon - local_time_array.tm_mon == 0:
                    if post_time_array.tm_mday - local_time_array.tm_mday == 0:
                        if post_time_array.tm_hour - local_time_array.tm_hour == 0:
                            order['time'] = str(local_time_array.tm_min - post_time_array.tm_min) + u"分钟前"
                        else:
                            order['time'] = str(local_time_array.tm_hour - post_time_array.tm_hour) + u"小时前"
                    else:
                        order['time'] = str(local_time_array.tm_mday - post_time_array.tm_mday) + u"天前"
                else:
                    order['time'] = str(local_time_array.tm_mon - post_time_array.tm_mon) + u"月前"
            else:
                post_orders[0]['time'] = str(local_time_array.tm_year - post_time_array.tm_year) + u"年前"
        for order in get_orders:
            get_time_array = time.strptime(order['time'], u"%Y年%m月%d日%H时%M分")
            if get_time_array.tm_year - local_time_array.tm_year == 0:
                if get_time_array.tm_mon - local_time_array.tm_mon == 0:
                    if get_time_array.tm_mday - local_time_array.tm_mday == 0:
                        if get_time_array.tm_hour - local_time_array.tm_hour == 0:
                            order['time'] = str(local_time_array.tm_min - get_time_array.tm_min) + u"分钟前"
                        else:
                            order['time'] = str(local_time_array.tm_hour - get_time_array.tm_hour) + u"小时前"
                    else:
                        order['time'] = str(local_time_array.tm_mday - get_time_array.tm_mday) + u"天前"
                else:
                    order['time'] = str(local_time_array.tm_mon - get_time_array.tm_mon) + u"月前"
            else:
                order['time'] = str(local_time_array.tm_year - get_time_array.tm_year) + u"年前"
        for order in deal_orders:
            get_time_array = time.strptime(order['time'], u"%Y年%m月%d日%H时%M分")
            if get_time_array.tm_year - local_time_array.tm_year == 0:
                if get_time_array.tm_mon - local_time_array.tm_mon == 0:
                    if get_time_array.tm_mday - local_time_array.tm_mday == 0:
                        if get_time_array.tm_hour - local_time_array.tm_hour == 0:
                            order['time'] = str(local_time_array.tm_min - get_time_array.tm_min) + u"分钟前"
                        else:
                            order['time'] = str(local_time_array.tm_hour - get_time_array.tm_hour) + u"小时前"
                    else:
                        order['time'] = str(local_time_array.tm_mday - get_time_array.tm_mday) + u"天前"
                else:
                    order['time'] = str(local_time_array.tm_mon - get_time_array.tm_mon) + u"月前"
            else:
                order['time'] = str(local_time_array.tm_year - get_time_array.tm_year) + u"年前"
        return render_template('homePage.html', post_orders=post_orders, get_orders=get_orders, deal_orders=deal_orders,
                               user=user)
    else:
        return redirect(url_for('welcome'))


# 一键清除
@app.route('/clearNotification')
def clearNotification():
    g.db.execute('update user set notification = NULL, noticenum = 0 where username = ?', [session['username']])
    g.db.commit()
    return redirect(url_for('homePage'))


@app.route('/test/<username>')
def show_user_profile(username):
    return '你好 %s' % username


@app.route('/test/<int:post_id>')
def show_post(post_id):
    return '你投送了 %d' % post_id


@app.route('/location')
def showLocation():
    return render_template('showLocation.html')


@app.route('/hello')
def showHello():
    return render_template('showHello.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404


@app.route('/table')
def getTable():
    merchants = query_db('select * from merchant')
    commodity = query_db('select * from commodity')
    tariff = query_db('select * from tariff')
    return render_template("queryTable.html", orders=merchants, commoditys=commodity, tariffs=tariff)


@app.route('/table/removeMerchant', methods=['GET', 'POST'])
def removeMerchant():
    pid = request.form.get('id')
    # g.db.execute('delete from cart where id=?', [pid])
    # g.db.execute('delete from cart where id=?', [pid])
    # g.db.commit()

    return jsonify({"msg": "OK"})


@app.route('/t', methods=['GET', 'POST'])
def t():
    school = request.form.get("school")
    order_day1 = request.form.get("orderTime")
    order_day2 = request.form.get("orderTimeDay")
    order_day3 = request.form.get("orderTimeDay1")

    if school == u'复旦大学':

        m_num = query_db("select countDay as c_number from merchant where scope = '复旦南区'")
    else:
        m_num = query_db('select countDay as c_number from merchant where scope = ?', [school])

    m_num_n = m_num[0]["c_number"]
    days = [order_day1, order_day2, order_day3]

    flag_TD = {}
    flag_T = {}
    flag_T1 = {}

    for day in days:
        time_1_use = query_db(
            "select count(*) as number from cart where substr(dtime, 1, 4) = ? and scope = ? and substr(dtime,6,11)='12:00-12:45' ",
            [day, school])
        time_2_use = query_db(
            "select count(*) as number from cart where substr(dtime, 1, 4) = ? and scope = ? and substr(dtime,6,11)='12:45-13:30' ",
            [day, school])
        time_3_use = query_db(
            "select count(*) as number from cart where substr(dtime, 1, 4) = ? and scope = ? and substr(dtime,6,11)='18:00-18:45' ",
            [day, school])
        time_4_use = query_db(
            "select count(*) as number from cart where substr(dtime, 1, 4) = ? and scope = ? and substr(dtime,6,11)='18:45-19:30' ",
            [day, school])
        time_1_use_n = time_1_use[0]["number"]
        time_2_use_n = time_2_use[0]["number"]
        time_3_use_n = time_3_use[0]["number"]
        time_4_use_n = time_4_use[0]["number"]
        time1_flag = False
        time2_flag = False
        time3_flag = False
        time4_flag = False
        if time_1_use_n > m_num_n:
            time1_flag = True

        if time_2_use_n > m_num_n:
            time2_flag = True

        if time_3_use_n > m_num_n:
            time3_flag = True

        if time_4_use_n > m_num_n:
            time4_flag = True

        if day == order_day1:
            flag_TD = {day: {"time1_flag": time1_flag, "time2_flag": time2_flag, "time3_flag": time3_flag,
                             "time4_flag": time4_flag}}
        if day == order_day2:
            flag_T = {day: {"time1_flag": time1_flag, "time2_flag": time2_flag, "time3_flag": time3_flag,
                            "time4_flag": time4_flag}}
        if day == order_day3:
            flag_T1 = {day: {"time1_flag": time1_flag, "time2_flag": time2_flag, "time3_flag": time3_flag,
                             "time4_flag": time4_flag}}

    return jsonify({"flag_TD": flag_TD, "flag_T": flag_T, "flag_T1": flag_T1})


if __name__ == "__main__":
    app.run(debug=True)

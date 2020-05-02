#-*- coding=utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import MySQLdb
import os
import sys
import importlib
importlib.reload(sys)

app = Flask(__name__)

# 全局变量
username = "TJU"
userRole = "CUSTOMER"
notFinishedNum = 0

@app.route('/')
@app.route('/index')
def indexpage():
	return render_template('index.html')

# 登录页面
@app.route('/login')
def loginPage():
	return render_template('login.html')

# 个人中心页面
@app.route('/personal')
def personalPage():
    return render_template('personal.html')

# 修改个人信息页面
@app.route('/ModifyPersonalInfo', methods=['GET', 'POST'])
def ModifyPersonalInfo():
    msg=""
    if request.method == 'GET':
        return render_template('ModifyPersonalInfo.html', username=username)
    if request.method =='POST':
        # username = request.form['username']
        address = request.form['address']
        phonenum = request.form['phonenum']
        # 连接数据库，默认数据库用户名root，密码空
        db = MySQLdb.connect("localhost", "root", "", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        sql = "Update {} SET address = '{}', phone = '{}' where username = '{}'".format(userRole, address, phonenum, username)
        try:
            cursor.execute(sql)
            db.commit()
            # print("修改个人信息成功")
            msg="done"
        except ValueError as e:
            print("--->", e)
            print("修改个人信息失败")
            msg="fail"
        return render_template('ModifyPersonalInfo.html', messages=msg, username=username)

# 修改密码页面
@app.route('/ModifyPassword', methods=['GET', 'POST'])
def ModifyPassword():
    msg=""
    if request.method == 'GET':
        return render_template('ModifyPassword.html', username=username)
    if request.method =='POST':
        # username = request.form['username']
        psw1 = request.form['psw1']
        psw2 = request.form['psw2']
        # 两次输入密码是否相同
        if psw1 == psw2:
            # 连接数据库，默认数据库用户名root，密码空
            db = MySQLdb.connect("localhost", "root", "", "appDB", charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql = "Update {} SET password = '{}' where username = '{}'".format(userRole, psw1, username)
            try:
                cursor.execute(sql)
                db.commit()
                # print("修改密码成功")
                msg="done"
            except ValueError as e:
                print("--->", e)
                print("修改密码失败")
                msg="fail"
            return render_template('ModifyPassword.html', messages=msg, username=username)
        else:
            msg="not equal"
            return render_template('ModifyPassword.html', messages=msg, username=username)

@app.route('/OrderPage', methods=['GET', 'POST'])
def OrderPage():
    msg = ""
    global notFinishedNum
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = MySQLdb.connect("localhost", "root", "", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # 查询未完成订单数量
        presql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 0" % username
        cursor.execute(presql)
        res1 = cursor.fetchall()
        notFinishedNum = len(res1)
        # 查询其他信息
        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s'" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('OrderPage.html', username=username, result = res, messages=msg, notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
            return render_template('OrderPage.html', username=username, messages=msg)
    elif request.form["action"] == "按时间排序":
        db = MySQLdb.connect("localhost", "root", "", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        
        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' Order BY tansactiontime DESC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('OrderPage.html', username=username, result = res, messages=msg, notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('OrderPage.html', username=username, messages=msg)
    elif request.form["action"] == "按价格排序":
        db = MySQLdb.connect("localhost", "root", "", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        
        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' Order BY cost ASC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('OrderPage.html', username=username, result = res, messages=msg, notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('OrderPage.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "未完成订单":
        db = MySQLdb.connect("localhost", "root", "", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        
        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 0 " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('OrderPage.html', username=username, result = res, messages=msg, notFinishedNum=len(res))
        else:
            print("NULL")
            msg = "none"
        return render_template('OrderPage.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "确认收货":
        db = MySQLdb.connect("localhost", "root", "", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        print("用户要确认收货啦")
        orderID = request.form['orderID']
        print(orderID)
        sql = "Update ORDER_COMMENT SET isFinished = 1 WHERE orderID = '%s' " % orderID
        cursor.execute(sql)
        msg = "UpdateSucceed"
        return render_template('OrderPage.html', username=username, messages=msg)    
    else:
        return render_template('OrderPage.html', username=username, messages=msg)

@app.route('/MyComments', methods=['GET', 'POST'])
def MyCommentsPage():
    msg = ""
    global notFinishedNum
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = MySQLdb.connect("localhost", "root", "", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # 查询未完成及未评论订单数量
        presql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 0 OR text is null" % username
        cursor.execute(presql)
        res1 = cursor.fetchall()
        notFinishedNum = len(res1)
        # 查询其他信息
        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' and isFinished = 1 and text is not null" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MyComments.html', username=username, result = res, messages=msg, notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
            return render_template('MyComments.html', username=username, messages=msg)
    elif request.form["action"] == "按时间排序":
        db = MySQLdb.connect("localhost", "root", "", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        
        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text is not null Order BY tansactiontime DESC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MyComments.html', username=username, result = res, messages=msg, notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('MyComments.html', username=username, messages=msg)
    elif request.form["action"] == "按价格排序":
        db = MySQLdb.connect("localhost", "root", "", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        
        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text is not null Order BY cost ASC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MyComments.html', username=username, result = res, messages=msg, notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('MyComments.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "未评价订单":
        # TODO：这部分考虑去掉
        db = MySQLdb.connect("localhost", "root", "", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        
        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text is null" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MyComments.html', username=username, result = res, messages=msg, notFinishedNum=len(res))
        else:
            print("NULL")
            msg = "none"
        return render_template('MyComments.html', username=username, messages=msg, notFinishedNum=notFinishedNum)

    else:
        return render_template('MyComments.html', username=username, messages=msg)

@app.route('/WriteComments', methods=['GET', 'POST'])
def WriteCommentsPage():
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = MySQLdb.connect("localhost", "root", "", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # 查询未完成订单数量
        presql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 0" % username
        cursor.execute(presql)
        res1 = cursor.fetchall()
        notFinishedNum = len(res1)
        # 查询其他信息
        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s'" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result = res, messages=msg, notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
            return render_template('WriteComments.html', username=username, messages=msg)
    elif request.form["action"] == "按时间排序":
        db = MySQLdb.connect("localhost", "root", "", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        
        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' Order BY tansactiontime DESC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result = res, messages=msg, notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('WriteComments.html', username=username, messages=msg)
    elif request.form["action"] == "按价格排序":
        db = MySQLdb.connect("localhost", "root", "", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        
        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' Order BY cost ASC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result = res, messages=msg, notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('WriteComments.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "未完成订单":
        db = MySQLdb.connect("localhost", "root", "", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        
        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 0 " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result = res, messages=msg, notFinishedNum=len(res))
        else:
            print("NULL")
            msg = "none"
        return render_template('WriteComments.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    # elif request.form["action"] == "写评论":
    #     print("用户要评论啦")
    #     orderID = request.form['orderID']
    #     print(orderID)
    #     msg = "WriteRequest"
    #     return render_template('CommentForm.html', username=username, orderID=orderID, messages=msg)
    elif request.form["action"] == "确认收货":
        msg = "Confirm"
        return render_template('WriteComments.html', username=username, messages=msg)

    else:
        return render_template('WriteComments.html', username=username, messages=msg)

@app.route('/CommentForm', methods=['GET', 'POST'])
def CommentFormPage():
    msg = ""
    if request.form["action"] == "写评论":
        print("用户要评论啦")
        orderID = request.form['orderID']
        print(orderID)
        msg = "WriteRequest"
        print(msg)
        return render_template('CommentForm.html', username=username, orderID=orderID, messages=msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='9090')
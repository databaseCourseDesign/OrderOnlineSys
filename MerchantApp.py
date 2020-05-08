# -*- coding=utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import MySQLdb
import os
import sys
import importlib

importlib.reload(sys)

app = Flask(__name__)

# 全局变量
username = "res1"
userRole = "RESTAURANT"
notFinishedNum = 0


@app.route('/')
@app.route('/MerchantIndex')
def indexpage():
    return render_template('MerchantIndex.html')


# 登录页面
@app.route('/login')
def loginPage():
    return render_template('login.html')


# 个人中心页面
@app.route('/MerchantPersonal')
def personalPage():
    return render_template('MerchantPersonal.html')


# 修改个人信息页面
@app.route('/MerchantModifyPerInfo', methods=['GET', 'POST'])
def MerchantModifyPerInfo():
    msg = ""
    if request.method == 'GET':
        return render_template('MerchantModifyPerInfo.html', username=username)
    if request.method == 'POST':
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
        sql = "Update {} SET address = '{}', phone = '{}' where username = '{}'".format(userRole, address, phonenum,
                                                                                        username)
        try:
            cursor.execute(sql)
            db.commit()
            # print("修改个人信息成功")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("修改个人信息失败")
            msg = "fail"
        return render_template('MerchantModifyPerInfo.html', messages=msg, username=username)


# 修改密码页面
@app.route('/MerchantModifyPwd', methods=['GET', 'POST'])
def ModifyPassword():
    msg = ""
    if request.method == 'GET':
        return render_template('MerchantModifyPwd.html', username=username)
    if request.method == 'POST':
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
                msg = "done"
            except ValueError as e:
                print("--->", e)
                print("修改密码失败")
                msg = "fail"
            return render_template('MerchantModifyPwd.html', messages=msg, username=username)
        else:
            msg = "not equal"
            return render_template('MerchantModifyPwd.html', messages=msg, username=username)


@app.route('/MerchantOrderPage', methods=['GET', 'POST'])
def MerchantOrderPage():
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
        presql = "SELECT * FROM ORDER_COMMENT WHERE restaurant = '%s' AND isFinished = 0" % username
        cursor.execute(presql)
        res1 = cursor.fetchall()
        notFinishedNum = len(res1)
        # 查询其他信息
        sql = "SELECT * FROM ORDER_COMMENT WHERE restaurant = '%s'" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MerchantOrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
            return render_template('MerchantOrderPage.html', username=username, messages=msg)
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
            return render_template('MerchantOrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('MerchantOrderPage.html', username=username, messages=msg)
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
            return render_template('MerchantOrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('MerchantOrderPage.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
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
            return render_template('MerchantOrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=len(res))
        else:
            print("NULL")
            msg = "none"
        return render_template('MerchantOrderPage.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    else:
        return render_template('MerchantOrderPage.html', username=username, messages=msg)


if __name__ == '__main__':
    app.run(host='localhost', port='5001')
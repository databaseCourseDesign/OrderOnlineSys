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
    if request.method == 'GET':
        return render_template('ModifyPersonalInfo.html', username=username)
    if request.method =='POST':
        msg=""
        # username = request.form['username']
        address = request.form['address']
        phonenum = request.form['phonenum']
        db = MySQLdb.connect("localhost", "root", "", "pandb", charset='utf8')
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
        return render_template('ModifyPersonalInfo.html', messages=msg)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='9090')
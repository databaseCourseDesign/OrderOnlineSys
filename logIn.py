# -*- coding=utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import MySQLdb
import os
import sys
import importlib

importlib.reload(sys)

app = Flask(__name__)
# 登录
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def registerPage():

	return render_template('index.html')

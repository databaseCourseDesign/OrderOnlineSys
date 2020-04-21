#-*- coding=utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import sys
import importlib
importlib.reload(sys)

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def indexpage():
	return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='9090')
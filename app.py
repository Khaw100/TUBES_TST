from appflask import app
from config import mysql
from flask import jsonify, flash, request, make_response
from functools import wraps
from urllib.request import urlopen
import requests
import json
import pymysql

@app.route('/')
def index():
    data = {"msg":"Selamat datang di service Pengelolaan Lamaran Kerja Google"}
    return jsonify(data)

@app.route('/a')
def a():

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM user_data")

if __name__ == "__main__":
    app.run()
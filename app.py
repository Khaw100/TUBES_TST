from appflask import app
from config import mysql
# from datauser import *

from flask import Flask, jsonify, request, render_template, make_response
from functools import wraps
from urllib.request import urlopen
from flaskext.mysql import MySQL
import requests
import json
import jwt
import datetime
import random
import pymysql

@app.route('/')
def index():
    data = {'message':"Selamat datang di Servis Pengelolaan Lamaran Kerja Google"}
    return jsonify(data)

app.config['SECRET_KEY'] ='dvp'
# tmp = []

# Token Required
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is Missing'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')

        except:
            return jsonify({'message': 'Token is Invalid'}), 403

        return f(*args, **kwargs)
    return decorated
    
# Login Account
@app.route('/login',methods=['GET','POST'])
def login():
    auth = request.authorization
    if auth and loginValidation(auth.username, auth.password) == True:
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, app.config['SECRET_KEY'])

        return jsonify({'Token': token})

    return make_response('Failed to verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    
def loginValidation(username, password):
    valid = False
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(f"SELECT * FROM user_data_dr where username = '{username}' and password = '{password}'")
    if cursor.rowcount > 0:
        valid = True
    cursor.close()
    conn.close()
    return valid

# Define the app
@app.route("/read",methods=['GET','POST'])
@token_required
def read():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute("SELECT Category, Responsibilities, Title FROM job_skills_rakha WHERE Location LIKE '% Brazil' AND Category = 'Software Engineering'")
    data = cursor.fetchall()
    return jsonify(data)

################################################### Provide Data For Dapeb ############################################################

@app.route('/get-jobs-by-category/<categorypick>')
@token_required
def getJobsByCategory(categorypick):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(f"SELECT Title, Location, Category, Responsibilities FROM job_skills_rakha WHERE Category = '{categorypick}' LIMIT 5")
        data = cursor.fetchall()
        return jsonify(data)
    except Exception as e:
        print(e)
        return jsonify({"msg":"Data tidak ditemukan"})
    
    finally:
        cursor.close()
        conn.close()
        
@app.route('/get-jobs-by-location/<locationpick>')
@token_required
def getJobsByLocation(locationpick):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(f"SELECT Title, Location, Category, Responsibilities FROM job_skills_rakha WHERE Location LIKE '% {locationpick}' LIMIT 5")
        data = cursor.fetchall()
        return jsonify(data)
    except Exception as e:
        print(e)
        return jsonify({"msg":"Data tidak ditemukan"})
    
    finally:
        cursor.close()
        conn.close()
        
######################### CORE API #############################################################################################
def get_token_by_login():
    url = 'http://rakha:password@wipeeeb.my.id/test/login'
    response = requests.get(url)
    response = (response.json())    
    token = response['Token']
    return token
    
def get_my_token():
    url = 'http://rakha:password@wipeeeb.my.id/manage-job-applicants/login'
    response = requests.get(url)
    response = (response.json())    
    token = response['Token']
    return token

def get_countries():
    LIST_COUNTRY = []
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT city FROM `living_cost` WHERE city LIKE '%, Germany'")
        read_row = cursor.fetchall()
        
        for row in read_row:
            country = row['Location'].split(',')[-1]
            LIST_COUNTRY.append(country)
        return LIST_COUNTRY

    except Exception as e:
        print(e)
        return []

    finally:
        cursor.close()
        conn.close()

@app.route('/management-job-seekers/<country>/<rolefirst>/<rolelast>/orang')
def managementJobSeeker(country, rolefirst, rolelast):
    arrNama = []
    arrTitle = []
    token = get_token_by_login()
    url = "http://wipeeeb.my.id/test/jobseekers/" + country + "/" + rolefirst + "/" + rolelast + "?token=" + str(token)
    dataresponse = urlopen(url)
    dataresponse = json.loads(dataresponse.read())
    n = len(dataresponse)
    for data in dataresponse:
        x = data['Name']
        arrNama.append(x)
        
    my_token = get_my_token()
    my_url = "http://wipeeeb.my.id/manage-job-applicants/getJob/" + country + "/" + rolefirst + "/" + rolelast + "?token=" + str(token)
    my_data = urlopen(my_url)
    my_data = json.loads(my_data.read())
    n = len(my_data)
    for data in my_data:
        x = data['Title']
        arrTitle.append(x)
    return jsonify({'Title':arrTitle,'Name': arrNama})
    

@app.route('/jumlah/<country>/<rolefirst>/<rolelast>')
def jumlahJobSeeker(country, rolefirst, rolelast):
    arrNama = []
    arrTitle = []
    token = get_token_by_login()
    url = "http://wipeeeb.my.id/test/jobseekers/" + country + "/" + rolefirst + "/" + rolelast + "?token=" + str(token)
    dataresponse = urlopen(url)
    dataresponse = json.loads(dataresponse.read())
    n = len(dataresponse)
    
    my_token = get_my_token()
    my_url = "http://wipeeeb.my.id/manage-job-applicants/getJob/" + country + "/" + rolefirst + "/" + rolelast + "?token=" + str(token)
    my_data = urlopen(my_url)
    my_data = json.loads(my_data.read())
    n = len(my_data)
    for data in my_data:
        x = data['Title']
        arrTitle.append(x)
    
    return jsonify({'Title':arrTitle,"Jumlah": n})




###################ssss

@app.route('/getJob/<country>/<rolefirst>/<rolelast>')
@token_required
def getJobseekers(country, rolefirst, rolelast):
    arrParameter = []
    arrPositionParameter = []
    if str(country) != 'f':
        arrParameter += [str(country)]
        arrPositionParameter += [1]
    if str(rolefirst) != 'f':
        if str(rolelast) != 'f':
            arrParameter += [str(str(rolefirst)+" "+str(rolelast))]
            arrPositionParameter += [3]
        else:
            arrParameter += [str(rolefirst)]
            arrPositionParameter += [2]
    if str(rolelast) != 'f':
        if str(rolefirst) != 'f':
            arrParameter += [str(str(rolefirst)+" "+str(rolelast))]
            arrPositionParameter += [3]
        else:
            arrParameter += [str(rolelast)]
            arrPositionParameter += [3]

        
    queryselect = "SELECT Category, Responsibilities, Title, Location FROM job_skills_rakha WHERE"

    querycondition = ""
    for i in range(len(arrParameter)):
        if arrPositionParameter[i] == 1:
            if i != 0:
                querycondition = querycondition + " AND "
            querycondition = querycondition + " Location LIKE '% " + arrParameter[i] + "' "
        if arrPositionParameter[i] == 2:
            if i != 0:
                querycondition = querycondition + " AND "
            querycondition = querycondition + "  Category LIKE '" + arrParameter[i] + "%' "
        if arrPositionParameter[i] == 3:
            if i != 0:
                querycondition = querycondition + " AND "
            querycondition = querycondition + " Category LIKE '%" + arrParameter[i] + "' "

    queryfinal = queryselect + querycondition
    # return jsonify(queryfinal)  
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(queryfinal)
        read_row = cursor.fetchall()
        response = jsonify(read_row)
        response.status_code = 200
        return response
    except Exception as e:
        return jsonify(e)
    finally:
        cursor.close()
        conn.close()

###################SSS

if __name__ == "__main__":
    app.run()
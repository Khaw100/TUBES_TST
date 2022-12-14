from flask import jsonify, request, make_response, render_template, redirect
from functools import wraps

from appflask import app
from config import mysql

from flask_mail import Mail,Message 
import jwt
import datetime
import random
import pymysql

mail = Mail(app)
userData = {
    "email": '',
    "otp": ''
}
dctUserData = {}


@app.route('/login')
def login():
    # conn = mysql.connect()
    # cursor = conn.cursor(pymysql.cursors.DictCursor)
    # cursor.execute("SELECT * FROM account_client")
    # read_row = cursor.fetchone()
    # cursor.close()
    # conn.close()
    # return jsonify(read_row)
    # username = request.values.get('username')
    # password = request.values.get('password')
    # username = "rakha"
    # password = "diamond"
    auth = request.authorization
    if auth and loginValidation(auth.username, auth.password):
        token = jwt.encode({'user':auth.username, 'exp':datetime.datetime.utcnow()+datetime.timedelta(seconds=10)},app.config['SECRET_KEY'])
        return jsonify({'Token': token})
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})




# make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
# @app.route('/register')
# def register():
#     render_template('register.html')

# @app.route('/verify',methods=['GET','POST'])
# def verify():
#     conn = mysql.connect()
#     cur = conn.cursor(pymysql.cursors.DictCursor)
#     dusername = request.form['dusername']
#     dpassword = request.form['dpassword']
#     email = request.form['email']
#     dctUserData[dusername] = dpassword
#     print(dctUserData)
#     print(dctUserData[dusername])
#     userData['email'] = email
#     query = f"INSERT INTO user_data VALUES ('{dusername}', '{dpassword}')"
#     cur.execute(query)
#     mysql.connection.commit()

#     msg = Message('Confirm Email',recipients=[email])
#     otp = generateOTP()
#     userData['otp'] = otp
#     msg.body = f'Hello your OTP is: {otp}'
#     mail.send(msg)
#     return render_template('verify.html')

# @app.route('/validate',methods=['POST'])
# def validate():
#     userOTP = request.form['otp']
#     if userData['otp'] == userOTP:
#         return redirect("/login")
#     else:
#         return 'OTP salah'



# Function

# Login Validation
def loginValidation(username, password):
    valid = False
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM user_data where username = '" + username + "' and password = '" + password + "'")
    if cursor.rowcount > 0:
        return True
    cursor.close()
    conn.close()
    return valid

# Generate OTP
def generateOTP():
    finalOTP= ''
    for i in range (4):
        finalOTP = finalOTP + str(random.randint(0,9))
    return finalOTP

# Token Required 
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token == 0:
            return jsonify({'message':'Token is missing'}),403
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])
        except:
            return jsonify({'message':'Token is invalid'}),403
        return f(*args,**kwargs)
    return decorated
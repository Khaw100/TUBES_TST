# import pymysql
# from flask import jsonify

# from appflask import app
# from config import mysql
# from app import token_required

# @app.route('/get-jobs-by-location/<location>')
# # @token_required
# def getLivingCostFromCity(location):
#     try:
#         conn = mysql.connect()
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#         cursor.execute(f"SELECT Title, Location, Category, Responsibilitites FROM job_skills WHERE Location LIKE '% {location}'")
#         read_row = cursor.fetchall()
#         data = { "Job_data" : read_row, "msg" : "Data berhasil ditemukan" }
    
#         response = jsonify(data)
#         response.status_code = 200
#         return response
    
#     except Exception as e:
#         print(e)
#         return jsonify({"msg" : "Data tidak ditemukan"})
    
#     finally:
#         cursor.close()
#         conn.close()

# @app.route('/get-jobs-by-category/<category>')
# @token_required
# def getLivingCostFromCity(category):
#     try:
#         conn = mysql.connect()
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#         cursor.execute(f"SELECT Title, Location, Category, Responsibilitites FROM job_skills WHERE Category = '{category}'")
#         read_row = cursor.fetchall()
#         data = { "Job_data" : read_row, "msg" : "Data berhasil ditemukan" }
    
#         response = jsonify(data)
#         response.status_code = 200
#         return response
    
#     except Exception as e:
#         print(e)
#         return jsonify({"msg" : "Data tidak ditemukan"})
    
#     finally:
#         cursor.close()
#         conn.close()

# @app.route('/get-jobs-by-category-location/<category>/<location>')
# # @token_required
# def getLivingCostFromCity(category,location):
#     try:
#         conn = mysql.connect()
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#         cursor.execute(f"SELECT Title, Location, Category, Responsibilitites FROM job_skills WHERE Category = '{category}' AND Location LIKE '% {location}'")
#         read_row = cursor.fetchall()
#         data = { "Job_data" : read_row, "msg" : "Data berhasil ditemukan" }
    
#         response = jsonify(data)
#         response.status_code = 200
#         return response
    
#     except Exception as e:
#         print(e)
#         return jsonify({"msg" : "Data tidak ditemukan"})
    
#     finally:
#         cursor.close()
#         conn.close()
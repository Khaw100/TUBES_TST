from appflask import app
from flaskext.mysql import MySQL

mysql = MySQL()

app.config['JSON_SORT_KEYS'] = False
app.config['MYSQL_USER'] = 'wipeeebm_rakha'
app.config['MYSQL_PASSWORD'] = 'Miscrit10'
app.config['MYSQL_DB'] = 'wipeeebm_Google_Data'
app.config['MYSQL_HOST'] = '103.163.138.244'

# app.config['JSON_SORT_KEYS'] = False
# app.config['MYSQL_USER'] = 'wakacipu_kafi'
# app.config['MYSQL_PASSWORD'] = '7601labtek5'
# app.config['MYSQL_DB'] = 'wakacipu_livingcost'
# app.config['MYSQL_HOST'] = '103.163.138.244'


# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_USERNAME']= 'rakhawiratama10@gmail.com'
# app.config['MAIL_PASSWORD'] = 'byhhhozgycuhalth'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL']= True
# app.config['MAIL_USE_TLS'] = False

# app.config.update(
#     MAIL_SERVER='smtp.gmail.com',
#     MAIL_USERNAME='rakhawiratama10@gmail.com',
#     MAIL_PASSWORD = 'byhhhozgycuhalth',
#     MAIL_PORT = 465,
#     MAIL_USE_SSL=True,
#     MAIL_USE_TLS = False,
# )
mysql.init_app(app)
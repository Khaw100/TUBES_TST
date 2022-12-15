from appflask import app
from flaskext.mysql import MySQL

app.config['MYSQL_DATABASE_USER'] = 'wakacipu_kafi'
app.config['MYSQL_DATABASE_PASSWORD'] = '7601labtek5'
app.config['MYSQL_DATABASE_DB'] = 'wakacipu_livingcost'
app.config['MYSQL_DATABASE_HOST'] = '103.163.138.244'
app.config['SECRET_KEY'] = 'gfseeker'

mysql = MySQL()

mysql.init_app(app)
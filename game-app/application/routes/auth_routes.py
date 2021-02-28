from flask import Blueprint,render_template,g,request,jsonify
from flask import current_app as app
from application.sql_queries.sql_statements import app_queries
#sys.path.insert(-1,'/usr/local/lib/python3.7/site-packages')
from mysql_conn.connect_mysql import get_connection
import base64
from pathlib import Path

auth_bp = Blueprint('auth_bp',__name__,static_folder='static')

@auth_bp.before_request
def before_request():
	g.db = get_connection()
	query = '''select id,console_name,console_shortname,coalesce(twitter,'') as twitter,coalesce(facebook,'') as facebook from auths.auth_console;'''
	g.menu = g.db.select_no_params(query)
	g.menu_title = 'Game Consoles'

@auth_bp.after_request
def after_request(resp):
	g.db.close_connection()
	return resp

@auth_bp.route('/',methods=['GET'])
@auth_bp.route('/login/',methods=['GET'])
def home():
	return render_template('auth/index.html',title='Login',menu=g.menu[1],body='home',menu_title = g.menu_title)

@auth_bp.route('/logout/',methods=['GET'])
def two():
	return 'This is dfact/two route'


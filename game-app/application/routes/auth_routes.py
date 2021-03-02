from flask import Blueprint,render_template,g,request,jsonify
from flask import current_app as app
from application.sql_queries.sql_statements import app_queries
#sys.path.insert(-1,'/usr/local/lib/python3.7/site-packages')
from mysql_conn.connect_mysql import get_connection
import base64
from pathlib import Path
import random

auth_bp = Blueprint('auth_bp',__name__,static_folder='static')

@auth_bp.before_request
def before_request():
	g.db = get_connection()
	query = '''select id,console_name,console_shortname,coalesce(twitter,'') as twitter,coalesce(facebook,'') as facebook from games.game_console;'''
	g.menu = g.db.select_no_params(query)
	g.menu_title = 'Game Consoles'

@auth_bp.after_request
def after_request(resp):
	g.db.close_connection()
	return resp

@auth_bp.route('/',methods=['GET'])
@auth_bp.route('/login/',methods=['GET'])
def home():
	item = random.randrange(0,len(g.menu[1]),1)
	sn = g.menu[1][item]['console_shortname']
	query = '''select c.id as console_id,v.id,v.name,v.small_image,v.large_image 
           from games.game_console as c inner join games.video_games as v on v.console_id = c.id 
           where c.id = %s order by v.name;'''
	results = g.db.select_params(query,[g.menu[1][item]['id']])
	game_len = random.randrange(0,len(results[1]),)
	return render_template('auth/index.html',title='Login',menu=g.menu[1],body='home',menu_title = g.menu_title,data = [results[1][game_len]],shortname=sn)

@auth_bp.route('/logout/',methods=['GET'])
def two():
	return 'This is dfact/two route'


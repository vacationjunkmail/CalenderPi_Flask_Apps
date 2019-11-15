#import sys 
#sys.path.insert(-1,'/usr/local/lib/python3.4/site-packages')
from flask import Blueprint, render_template, session, redirect, url_for, request, flash, g, jsonify, abort
#from flask_wtf.csrf import CSRFProtect, CSRFError
from mysql_conn.connect_mysql import get_connection

#https://commons.wikimedia.org/wiki/Nintendo

games = Blueprint('games', __name__)

@games.before_request
def before_request():
	g.mysql_db = get_connection()
	

@games.after_request
def after_request(resp):
	g.mysql_db.close_connection()
	return resp


@games.route('/games/')
def index():
	
	query = 'select id,console_name,console_shortname from games.game_console;'
	results = g.mysql_db.select_no_params(query)
	return render_template('games/games.html',menu = results[1], title = 'Game Consoles')

@games.route('/games/<int:console_id>/')
def show_all_games(console_id):

	query = 'select id,console_name,console_shortname from games.game_console;'
	menu = g.mysql_db.select_no_params(query)
	
	query = 'select id, console_name,console_shortname from games.game_console where id = %s'
	params = [console_id]
	console_results = g.mysql_db.select_params(query,params)
	query = '''select c.id as console_id,v.id,v.name,v.small_image,v.large_image 
		   from games.game_console as c inner join games.video_games as v on v.console_id = c.id 
	 	   where c.id = %s'''
	results = g.mysql_db.select_params(query,params)
	print(console_results[1][0]['console_shortname'])
	return render_template('games/show_all_games.html', menu = menu[1],title = console_results[1][0]['console_name'],shortname = console_results[1][0]['console_shortname'],data = results[1])

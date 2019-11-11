#import sys 
#sys.path.insert(-1,'/usr/local/lib/python3.4/site-packages')
from flask import Blueprint, render_template, session, redirect, url_for, request, flash, g, jsonify, abort
#from flask_wtf.csrf import CSRFProtect, CSRFError
from mysql_conn.connect_mysql import get_connection

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
	print(results)
	return render_template('games/games.html',menu = results[1], title = 'Game Consoles')

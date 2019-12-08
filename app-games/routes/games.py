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
	query = '''select id,console_name,console_shortname,coalesce(twitter,'') as twitter,coalesce(facebook,'') as facebook from games.game_console;'''
	g.menu = g.mysql_db.select_no_params(query)
	

@games.after_request
def after_request(resp):
	g.mysql_db.close_connection()
	return resp


@games.route('/games/')
def index():
	
	return render_template('games/games.html',menu = g.menu[1], title = 'Game Consoles')

@games.route('/games/<int:console_id>/')
def show_all_games(console_id):
	
	params = [console_id]
	console_results = find_game_data(g.menu[1],console_id)
	query = '''select c.id as console_id,v.id,v.name,v.small_image,v.large_image 
		   from games.game_console as c inner join games.video_games as v on v.console_id = c.id 
	 	   where c.id = %s order by v.name;'''
	results = g.mysql_db.select_params(query,params)
	return render_template('games/show_all_games.html', menu = g.menu[1],title = console_results[0]['console_name'],shortname = console_results[0]['console_shortname'],data = results[1],twitter = console_results[0]['twitter'], facebook = console_results[0]['facebook'])

@games.route('/games/<int:console_id>/<int:game_id>/')
def single_game(console_id,game_id):

	params = [console_id]
	game_data = find_game_data(g.menu[1],console_id)
	header_image = "{}/{}_logo.png".format(game_data[0]['console_shortname'],game_data[0]['console_shortname'])
	shortname = game_data[0]['console_shortname']
	title = game_data[0]['console_name']
	params.append(game_id)
	query = '''select c.id as console_id,v.id,v.name,v.small_image,v.large_image,v.header_image
		   from games.game_console as c inner join games.video_games as v on v.console_id = c.id
                   where c.id = %s and v.id = %s;'''
	results = g.mysql_db.select_params(query,params)

	if results[1][0]['header_image']:
		header_image = "{}/header/{}".format(shortname,results[1][0]['header_image'])

	params = [game_id]
	query = '''select c.name from games.characters as c inner join games.video_game_and_characters as v on v.character_id =c.id  
		   where video_game_id = %s order by c.order_num,c.name;'''
	characters = g.mysql_db.select_params(query,params)
	return render_template('games/single_game.html',menu = g.menu[1],title = title,shortname = shortname,data = results[1],characters = characters[1],twitter = game_data[0]['twitter'], facebook = game_data[0]['facebook'],header_image = header_image)

def find_game_data(query,id):
	data_list = []
	for item in query:
		if item['id'] == id:
			data_list.append(item)
			break
	return data_list



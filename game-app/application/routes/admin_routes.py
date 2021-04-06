from flask import Blueprint,render_template,g,jsonify,json,request,url_for,redirect
from flask import current_app as app, flash,jsonify
from mysql_conn.connect_mysql import get_connection
from application.sql_queries.sql_statements import app_queries
import requests
#import mysql_conn
admin_bp = Blueprint('admin_bp',__name__,static_folder='static')

@admin_bp.before_request
def before_request():
	#print(mysql_conn.__file__)
	g.db = get_connection()
	query = '''select concat('admin/',table_name) as id,table_name as console_shortname from information_schema.tables 
		where table_schema='games' and table_name <> 'video_game_and_characters' order by table_name;'''
	g.menu = g.db.select_no_params(query)
	g.menu_title = 'Admin Sections'
	g.console_query = g.db.select_no_params('select id,console_shortname from games.game_console;')

@admin_bp.after_request
def after_request(resp):
	g.db.close_connection()
	return resp

@admin_bp.route('/',methods=['GET'])
def home():
	return render_template('admin/admin_index.html', title='Admin Home',menu=g.menu[1],menu_title=g.menu_title)

@admin_bp.route('/<string:url_route>/<int:pageid>/',methods=['GET','POST'])
@admin_bp.route('/<string:url_route>/',methods=['GET','POST'])
def base_index(url_route,pageid=0):
	#pageid = 0
	if request.method == 'POST':
		fetchapi = request.get_json()
		if fetchapi:
			pageid = fetchapi['pageid']
		else:
			pageid=request.form['pageid']
	statement = app_queries.base_index(url_route)
	page = 'admin/{}_index.html'.format(url_route)
	data = g.db.select_params(statement,[pageid])
	title = url_route.replace("_"," ")
	consoles = {}

	for item in g.console_query[1]:
		consoles[item['id']] = item['console_shortname']
	if request.method == 'POST':
		return jsonify(data,consoles)
	else:
		return render_template(page,data = data,title = title,menu = g.menu[1],menu_title = g.menu_title,console = consoles,pageid=pageid)

@admin_bp.route('/game_console/<int:console_id>/',methods=['GET'])
def console_index(console_id):
	statement = app_queries.get_console()
	params = [console_id]
	data = g.db.select_params(statement,params)
	return render_template('admin/console_update.html',data = data[1],menu = g.menu[1],title = 'Console Update',menu_title = g.menu_title)

@admin_bp.route('/game_console/console_update/',methods=['POST'])
def console_update():
	statement = app_queries.update_console()
	params = [request.form['console_name'],request.form['console_shortname'],request.form['twitter'],request.form['facebook'],request.form['id']]
	status = g.db.update_statement(statement,params)
	message = "{} {}".format(params[0],status)	
	flash(message)
	return redirect(url_for('admin_bp.base_index',url_route='game_console'))

#admin_bp.route('/video_games/<int:vid_id>/<int:page_id>/')
@admin_bp.route('/video_games/<int:vid_id>/<int:page_id>/',methods=['GET'])
#def game_update(vid_id,page_id=None)
def game_update(vid_id,page_id):
	statement = app_queries.select_game()
	data = g.db.select_params(statement,[vid_id])
	statement = app_queries.select_characters()
	char_data = g.db.select_params(statement,[vid_id])
	statement = app_queries.select_comments()
	comment_data = g.db.select_params(statement,[vid_id])
	mytitle = "Update {}".format(data[1][0]['name'])
	statement = app_queries.next_game()
	nextid_data = g.db.select_params(statement,[vid_id])
	nextid = 0
	nextlimit = 0
	if len(nextid_data[1]) > 0:
		nextid = nextid_data[1][0]['id']
		nextlimit = round(nextid/50) * 50
	return render_template('admin/video_game_update.html',data = data[1],menu = g.menu[1],menu_title=g.menu_title,title=mytitle,consoles=g.console_query[1],
	char_data = char_data[1],comments = comment_data[1],pageid=page_id,nextid=nextid,nextlimit=nextlimit)


@admin_bp.route('/video_games/action/',methods=['Post'])
def update_game():
	statement = app_queries.game_update()
	params = [request.form['title'],request.form['console_id'],request.form['small_image'],request.form['large_image'],request.form['header_image']]
	params.append(request.form['game_desc'])
	params.append(request.form['id'])
	status = g.db.update_statement(statement,params)
	message = "{} {}".format(params[0],status)	
	pageid = request.form['pageid']
	flash(message)
	return redirect(url_for('admin_bp.base_index',url_route='video_games',pageid=pageid))

@admin_bp.route('/video_games/rm_char/')
def rm_char():
	id = request.args.get('id')
	video_game_id = request.args.get('game_id')
	params = [id,video_game_id]
	statement = app_queries.delete_character()
	results = g.db.mod_statement(statement,params,'delete')
	return jsonify(results)

@admin_bp.route('/video_games/add_character/',methods=['POST'])
def add_character():
	results = {}
	for item in request.form:
		results[item] = request.form[item]
	params = [results['game_id'],results['character_id']]
	statement = app_queries.insert_video_game_and_character()
	g.db.mod_statement(statement,params,'insert')
	return jsonify(results)

@admin_bp.route('/video_games/add_new_character/',methods=['POST'])
def add_new_character():
	results = {}
	results['game_id'] = request.form['game_id']
	results['character_name'] = request.form['character_name']
	statement = app_queries.insert_new_character()
	g.db.mod_statement(statement,[results['character_name']],'insert')
	statement = app_queries.get_character()
	char_data = g.db.select_params(statement,[results['character_name']])
	params = [results['game_id'],char_data[1][0]['id']]
	statement = app_queries.insert_video_game_and_character()
	g.db.mod_statement(statement,params,'insert')
	results['character_id'] = char_data[1][0]['id']
	return jsonify(results)

@admin_bp.route('/video_games/add_comment/',methods=['POST'])
def add_comment():
	results = {}
	results['game_id'] = request.form['game_id']
	results['comment'] = request.form['comment']
	params = [results['game_id'],results['comment']]
	statement = app_queries.insert_comment()
	return_data = g.db.mod_statement(statement,params,'insert')
	results['comment_id'] = return_data[1].lastrowid
	return jsonify(results)


@admin_bp.route('/characters/edit_characters/',methods=['POST'])
def edit_character():
	statement = app_queries.update_character()
	params = [request.form['character_name'],request.form['display_order'],request.form['id']]
	status = g.db.update_statement(statement,params)		
	return jsonify({'msg':status})


@admin_bp.route('/search_video_games/',methods=['POST'])
def game_search():
	#pageid = 0
	fetchapi = request.get_json()
	value = fetchapi['search']
	print(value)	
	#statement = app_queries.base_index(url_route)
	#page = 'admin/{}_index.html'.format(url_route)
	#data = g.db.select_params(statement,[pageid])
	#title = url_route.replace("_"," ")
	data = {'data':value}

	#for item in g.console_query[1]:
		#consoles[item['id']] = item['console_shortname']
	return jsonify(data)

from flask import Blueprint,render_template,g,jsonify,json,request,url_for,redirect
from flask import current_app as app, flash,jsonify
from mysql_conn.connect_mysql import get_connection
from application.sql_queries.sql_statements import app_queries
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

@admin_bp.route('/<string:url_route>/',methods=['GET'])
def base_index(url_route):
	statement = app_queries.base_index(url_route)
	page = 'admin/{}_index.html'.format(url_route)
	data = g.db.select_no_params(statement)
	title = url_route.replace("_"," ")
	consoles = {}
	#flash('Show me')
	for item in g.console_query[1]:
		consoles[item['id']] = item['console_shortname']
	return render_template(page,data = data,title = title,menu = g.menu[1],menu_title = g.menu_title,console = consoles)

@admin_bp.route('/game_console/<int:console_id>/',methods=['GET'])
def console_update(console_id):
	query ='select * from games.game_console where id = %s'
	params = [console_id]
	data = g.db.select_params(query,params)
	return render_template('admin/console_update.html',data = data[1],menu = g.menu[1])

@admin_bp.route('/video_games/<int:vid_id>/',methods=['GET'])
def game_update(vid_id):
	statement = app_queries.select_game()
	data = g.db.select_params(statement,[vid_id])
	statement = app_queries.select_characters()
	char_data = g.db.select_params(statement,[vid_id])
	return render_template('admin/video_game_update.html',data = data[1],menu = g.menu[1],menu_title=g.menu_title,title='Video Game Update',consoles=g.console_query[1],
	char_data = char_data[1])


@admin_bp.route('/video_games/action/',methods=['Post'])
def update_game():
	statement = app_queries.game_update()
	params = [request.form['title'],request.form['console_id'],request.form['small_image'],request.form['large_image'],request.form['header_image']]
	params.append(request.form['game_desc'])
	params.append(request.form['id'])
	status = g.db.update_statement(statement,params)
	message = "{} {}".format(params[0],status)	
	flash(message)
	for cname in request.form.getlist('newrow'):
		print(cname)	
	return redirect(url_for('admin_bp.base_index',url_route='video_games'))

@admin_bp.route('/video_games/rm_char/')
def rm_char():
	id = request.args.get('id')
	statement = app_queries.delete_character()
	results = g.db.mod_statement(statement,[id],'delete')
	return jsonify(results)

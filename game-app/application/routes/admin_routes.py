from flask import Blueprint,render_template,g,jsonify,json
from flask import current_app as app
from mysql_conn.connect_mysql import get_connection

admin_bp = Blueprint('admin_bp',__name__,static_folder='static')

@admin_bp.before_request
def before_request():
	g.db = get_connection()
	query = '''select concat('admin/',table_name) as id,table_name as console_shortname from information_schema.tables 
		where table_schema='games' and table_name <> 'video_game_and_characters' order by table_name;'''
	g.menu = g.db.select_no_params(query)

@admin_bp.after_request
def after_request(resp):
	g.db.close_connection()
	return resp

@admin_bp.route('/',methods=['GET'])
def home():
	return render_template('admin/admin_index.html', title='Admin Home',menu=g.menu[1],menu_title='Admin Sections')

@admin_bp.route('/<string:url_route>/',methods=['GET'])
def console_index(url_route):
	query ='''select * from games.{} limit 50;'''.format(url_route)
	page = 'admin/{}_index.html'.format(url_route)
	data = g.db.select_no_params(query)
	title = url_route.replace("_"," ")
	console_query = g.db.select_no_params('''select id,console_shortname from games.game_console;''')
	consoles = {}
	for item in console_query[1]:
		consoles[item['id']] = item['console_shortname']
	return render_template(page,data = data,title = title,menu = g.menu[1],menu_title = 'Admin Sections',console = consoles)

@admin_bp.route('/game_console/<int:console_id>/',methods=['GET'])
def console_update(console_id):
	query ='select * from games.game_console where id = %s'
	params = [console_id]
	data = g.db.select_params(query,params)
	return render_template('admin/console_update.html',data = data[1],menu = g.menu[1])


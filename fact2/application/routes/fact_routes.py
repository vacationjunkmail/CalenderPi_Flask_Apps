from flask import Blueprint,render_template,g
from flask import current_app as app
#sys.path.insert(-1,'/usr/local/lib/python3.7/site-packages')
from mysql_conn.connect_mysql import get_connection

fact_bp = Blueprint('fact_bp',__name__,static_folder='static')

@fact_bp.before_request
def before_request():
	g.db = get_connection()
	query = '''select id,console_name,console_shortname,coalesce(twitter,'') as twitter,coalesce(facebook,'') as facebook from games.game_console;'''
	g.menu = g.db.select_no_params(query)

@fact_bp.after_request
def after_request(resp):
	g.db.close_connection()
	return resp

@fact_bp.route('/',methods=['GET'])
def home():
	return render_template('fact2/index.html',title='Game App Factory Blueprint',menu=g.menu[1],body='home')

@fact_bp.route('/two/',methods=['GET'])
def two():
	return 'This is dfact/two route'

@fact_bp.route('/<int:console_id>/')
def show_all_games(console_id):
	
	params = [console_id]
	console_results = find_game_data(g.menu[1],console_id)
	query = '''select c.id as console_id,v.id,v.name,v.small_image,v.large_image 
		   from games.game_console as c inner join games.video_games as v on v.console_id = c.id 
	 	   where c.id = %s order by v.name;'''
	results = g.db.select_params(query,params)
	return render_template('fact2/show_all_games.html', menu = g.menu[1],title = console_results[0]['console_name'],shortname = console_results[0]['console_shortname'],data = results[1],twitter = console_results[0]['twitter'], facebook = console_results[0]['facebook'])

@fact_bp.route('/<int:console_id>/<int:game_id>/')
def single_game(console_id,game_id):

	params = [console_id]
	game_data = find_game_data(g.menu[1],console_id)
	header_image = "{}/{}_logo.png".format(game_data[0]['console_shortname'],game_data[0]['console_shortname'])
	shortname = game_data[0]['console_shortname']
	title = game_data[0]['console_name']
	params.append(game_id)
	query = '''select c.id as console_id,v.id,v.name,v.small_image,v.large_image,v.header_image,ifnull(v.game_description,'') as game_description
		   from games.game_console as c inner join games.video_games as v on v.console_id = c.id
                   where c.id = %s and v.id = %s;'''
	results = g.db.select_params(query,params)

	if results[1][0]['header_image']:
		header_image = "{}/header/{}".format(shortname,results[1][0]['header_image'])

	params = [game_id]
	query = '''select c.name from games.characters as c inner join games.video_game_and_characters as v on v.character_id =c.id  
		   where video_game_id = %s order by c.display_order,c.name;'''
	characters = g.db.select_params(query,params)
	return render_template('fact2/single_game.html',menu = g.menu[1],title = title,shortname = shortname,data = results[1],characters = characters[1],twitter = game_data[0]['twitter'], facebook = game_data[0]['facebook'],header_image = header_image)

def find_game_data(query,id):
	data_list = []
	for item in query:
		if item['id'] == id:
			data_list.append(item)
			break
	return data_list


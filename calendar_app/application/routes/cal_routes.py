from flask import Blueprint,render_template,g,jsonify,session,flash,redirect,url_for,request

from flask import current_app

from mysql_conn.connect_mysql import get_connection

cal_bp = Blueprint('cal_bp',__name__,template_folder='templates',static_folder='static')

@cal_bp.before_request
def before_request():
	g.db = get_connection()

@cal_bp.after_request
def after_request(resp):
	g.db.close_connection()
	return resp

@cal_bp.route('/calendar/',methods=['GET'])
def home():
	return render_template('calendar.html')

@cal_bp.route('/calendar_data/')
def calendar():
	events = []
	date_split = request.args['date'].split('/')
	params = [int(date_split[1]),int(date_split[0])]
	query = '''
	select `start_date` as start, `end_date` as end, `title` from dinner.menu_2 where month(`start_date`) = ? and year(`start_date`) = ?;
	'''
	data = g.db.select_params(query,params)
	return jsonify(data = data[1])

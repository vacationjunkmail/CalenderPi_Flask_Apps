from flask import Blueprint,render_template,g,jsonify,session,flash,redirect,url_for,request

from flask import current_app

from mysql_conn.connect_mysql import get_connection

script_bp = Blueprint('script_bp',__name__,template_folder='templates',static_folder='static')

@script_bp.before_request
def before_request():
	g.db = get_connection()

@script_bp.after_request
def after_request(resp):
	g.db.close_connection()
	return resp

@script_bp.route('/',methods=['GET'])
def home():
	data = []
	columns = []
	query = 'select id,`name`, "" as script from pythonscripts.scripts;'
	query = g.db.select_query(query)
	columns = query.column_names
	for recordset in query.fetchall():
		c = 0
		d = {}
		for row_value in recordset:
			if type(row_value) == int:
				d[columns[c]] = row_value
			else:
				try:
					d[columns[c]] = str(row_value.decode())
				except:
					d[columns[c]] = str(row_value)
			c += 1
		data.append(d)

	return render_template('pythonscripts.html',menu_data = data,menu_columns = columns)

@script_bp.route('/runscript/')
def runscript():
	os.system("python3 /home/pi/code/python/test.py")
	print('runscript route')
	return 'script ran'

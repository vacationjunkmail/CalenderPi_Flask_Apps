from flask import Blueprint,render_template,g,request,jsonify,session,current_app as app,flash,redirect,url_for
#from flask import current_app as app
from application.sql_queries.sql_statements import app_queries
#sys.path.insert(-1,'/usr/local/lib/python3.7/site-packages')
from mysql_conn.connect_mysql import get_connection
import base64
from pathlib import Path
import uuid

auth_bp = Blueprint('auth_bp',__name__,static_folder='static')

@auth_bp.before_request
def before_request():
	g.db = get_connection()
	g.menu_title = 'Game Consoles'

@auth_bp.after_request
def after_request(resp):
	g.db.close_connection()
	return resp

@auth_bp.route('/',methods=['GET'])
@auth_bp.route('/login/',methods=['GET'])
def login():
	return render_template('auth/index.html',title='Login',body='home',menu_title = g.menu_title)

@auth_bp.route('/login_check/',methods=['POST'])
def login_check():
	statement = app_queries.verify_user()
	params = [request.form['username'],request.form['password']]
	results = g.db.select_params(statement,params)
	if results[1]:
		for row in results[1]:
			session['id']= row['id']
			session['username'] = request.form['username']
		session['user-token'] = uuid.uuid4()
		return redirect(url_for('admin_bp.home'))
	else:
		session.clear()
		flash('Something went wrong')
		return render_template('auth/index.html',title='Login',body='',menu_title = g.menu_title)
			
@auth_bp.route('/logout/',methods=['GET'])
def logout():
	session.clear()
	flash('Logout Complete!')
	return redirect(url_for('game_bp.home'))


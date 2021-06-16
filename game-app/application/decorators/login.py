import time, socket, re
from functools import wraps
from application.functions import login_functions
from flask import session,redirect,url_for,request,g,current_app as app,flash
from urllib.parse import urlparse

def login_required(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'login_time' in session:
			minutes_passed = login_functions.diff_minutes(session['login_time'])
			if minutes_passed > 30:
				session['expired'] = "Session expired"
				return redirect(url_for('auth_bp.logout'))
		if 'user-token' in session:
			return f(*args,**kwargs)
		else:
			#for rule in app.url_map.iter_rules():
				#print(rule.rule)
			#for item in app.blueprints:
				#print(item)
			d = login_functions.host_regex(app.config['IP'],request.url)
			return redirect(url_for('auth_bp.login'))
	return wrap


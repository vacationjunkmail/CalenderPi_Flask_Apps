import time, socket, re
from functools import wraps

from flask import session,redirect,url_for,request,g,current_app as app
from urllib.parse import urlparse

def login_required(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'user-token' in session:
			return f(*args,**kwargs)
		else:
			#for rule in app.url_map.iter_rules():
				#print(rule.rule)
			#for item in app.blueprints:
				#print(item)
			session['next'] = re.sub(r':\d{4}','',request.url)
			return redirect(url_for('auth_bp.login'))
	return wrap


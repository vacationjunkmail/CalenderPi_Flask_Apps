import time, socket, re
from functools import wraps

from flask import session,redirect,url_for,request,g,current_app
from urllib.parse import urlparse

def login_required(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		print("here")
		if 'user-token' in session:
			return f(*args,**kwargs)
		else:
			return redirect(url_for('auth_bp.login'))
	return wrap


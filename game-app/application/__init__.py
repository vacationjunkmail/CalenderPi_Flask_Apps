from flask import Flask,render_template,request,flash
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def page_not_found(e):
	req_url = request.referrer
	bad_url = request.url
	req_path = "URL Route Does not Exist: {}".format(request.path)
	e = "Template Not Found: {}".format(e)
	flash(e)
	flash(req_path)
	return render_template('404.html'),404

def create_app():

	app = Flask(__name__,instance_relative_config=False)
	csrf.init_app(app)
	app.config.from_object('config.Config')
	app.register_error_handler(404,page_not_found)
	app.register_error_handler(500,page_not_found)
	
	with app.app_context():
		from .routes import admin_routes
		from .routes import game_routes
		#csrf.exempt(game_routes.game_bp)
		app.register_blueprint(admin_routes.admin_bp,url_prefix='/games/admin/')
		app.register_blueprint(game_routes.game_bp,url_prefix='/games/')
	return app

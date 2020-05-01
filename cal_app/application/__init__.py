from flask import Flask
from flask_wtf.csrf import CSRFProtect,CSRFError

def create_app():

	csrf = CSRFProtect()

	app = Flask(__name__,instance_relative_config=False)
	app.config.from_object('config.Config')
	csrf.init_app(app)
		
	with app.app_context():
		from .routes import index_routes
		from .routes import cal_routes
		from .routes import camera_routes
		from .routes import pyscripts_routes

		app.register_blueprint(index_routes.index_bp)
		app.register_blueprint(cal_routes.cal_bp)
		app.register_blueprint(pyscripts_routes.script_bp,url_prefix="/pythonscripts/")
		app.register_blueprint(camera_routes.camera_bp,url_prefix="/camera/")
	return app

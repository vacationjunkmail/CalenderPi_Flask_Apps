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
		app.register_blueprint(index_routes.index_bp)
		app.register_blueprint(cal_routes.cal_bp)
	return app

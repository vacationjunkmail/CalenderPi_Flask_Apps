from flask import Flask

def create_app():
	app = Flask(__name__, instance_relative_config=False)
	app.config.from_object('config.Config')
	
	with app.app_context():
		from . import routes
		#app.register_blueprint(auth.auth_bp)
		#app.register_blueprint(admin.admin_bp)
		
		return app
		

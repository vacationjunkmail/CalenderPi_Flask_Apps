from flask import Flask

def create_app():

	app = Flask(__name__,instance_relative_config=False)
	app.config.from_object('config.Config')
	
	with app.app_context():
		from .routes import admin_routes
		from .routes import fact_routes
		app.register_blueprint(admin_routes.admin_bp)
		app.register_blueprint(fact_routes.fact_bp)

	return app

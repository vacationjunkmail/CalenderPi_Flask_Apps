from flask import Flask
from flaskblog.config import Config

#app = Flask(__name__)
#@app.route('/hello')
#def index():
#	return 'help me'

#def create_app(config_class=Config):
def create_app():
    app = Flask(__name__)
    #app.config.from_object(Config)

    #db.init_app(app)
    #bcrypt.init_app(app)
    #login_manager.init_app(app)
    #mail.init_app(app)

    #from flaskblog.users.routes import users
    #from flaskblog.posts.routes import posts
    #from flaskblog.main.routes import main
    #app.register_blueprint(users)
    #app.register_blueprint(posts)
    #app.register_blueprint(main)
    print("test")    
    @app.route('/hello')
    def hello():
        return 'Hello'
    return app


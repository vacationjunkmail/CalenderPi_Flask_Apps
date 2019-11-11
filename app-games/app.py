import sys
sys.path.insert(-1,'/usr/local/lib/python3.4/site-packages')
#sys.path.insert(-1,'/home/pi/.local/lib/python3.4/site-packages')
from flask import Flask, jsonify, render_template, request, g, session, flash, redirect,url_for

from routes.games import games

app = Flask(__name__)

app.register_blueprint(games)

if __name__ == "__main__":
	app.run(host = '0.0.0.0', debug = True)

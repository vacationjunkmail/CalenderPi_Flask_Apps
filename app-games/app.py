import sys
sys.path.insert(-1,'/usr/local/lib/python3.4/site-packages')
#sys.path.insert(-1,'/home/pi/.local/lib/python3.4/site-packages')
#https://www.flaticon.com
from flask import Flask, jsonify, render_template, request, g, session, flash, redirect,url_for

from routes.games import games

app = Flask(__name__)

app.register_blueprint(games)

@app.errorhandler(502)
@app.errorhandler(500)
def not_found(e):
	print(e)
	return render_template("500.html")

@app.errorhandler(404)
def lost_template(e):
	return "template not found"

if __name__ == "__main__":
	app.run(host = '0.0.0.0', debug = True)

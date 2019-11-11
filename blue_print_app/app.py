from flask import Flask, jsonify, render_template, request, g, session, flash, redirect,url_for

from routes.l1 import l1
from routes.l2 import l2

app = Flask(__name__,static_url_path='/l1/static')

app.register_blueprint(l1)
app.register_blueprint(l2, url_prefix='/l1')
print(app.url_map)
if __name__ == "__main__":
	app.run(host = '0.0.0.0', debug = True)

from flask import Blueprint,render_template

from flask import current_app as app

main_bp = Blueprint('main_bp',__name__,template_folder='templates',static_folder='static')

@main_bp.route('/',methods=['GET'])
def home():
	return render_template('index.html',title='App Factory Blueprint',template='home-template main',body='home')

@main_bp.route('/two',methods=['GET'])
def two():
	return 'This is dfact/two route'

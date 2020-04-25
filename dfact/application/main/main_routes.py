from flask import Blueprint,render_template

from flask import current_app as app

main_bp = Blueprint('main_bp',__name__,template_folder='templates',static_folder='static')

@main_bp.route('/',methods=['GET'])
def home():
	return render_template('index.html',title='App Factory Blueprint',template='home template for main route',body='Routes are contained in their own folder.Templates are in subfolder of the routes folder.<br />Example:/main/templates/index.html')

@main_bp.route('/two',methods=['GET'])
def two():
	return 'This is dfact/two route'

from flask import Blueprint,render_template

from flask import current_app as app

admin_bp = Blueprint('admin_bp',__name__,static_folder='static')

@admin_bp.route('/admin')
@admin_bp.route('/add/',methods=['GET'])
def home():
	return render_template('admin/admin_index.html', title='admin index route',template='Admin blueprint main route',body='this is the body of the admin main route')

@admin_bp.route('/minus/',methods=['GET'])
def two():
	return 'This is dfact/admin/minus route'

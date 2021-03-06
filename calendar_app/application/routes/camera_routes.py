from flask import Blueprint,render_template,g,jsonify,session,flash,redirect,url_for,request
from flask import current_app
from picamera import PiCamera
from os import getcwd
from datetime import datetime
from time import sleep
from application.local_modules import check_file

from mysql_conn.connect_mysql import get_connection

camera_bp = Blueprint('camera_bp',__name__,template_folder='templates',static_folder='../../static')

@camera_bp.before_request
def before_request():
	g.db = get_connection()

@camera_bp.after_request
def after_request(resp):
	g.db.close_connection()
	return resp

@camera_bp.route('/',methods=['GET'])
def camera():
	if len(request.args):
		my_time = datetime.now()
		image_directory = "{}/static".format(getcwd())
		image_name = '_PiCamera_image.jpg';
	
		#remove file Function
		r = check_file.check_file_exists(image_directory,image_name)
		print("{} images removed".format(r))
		
		image_name = "{}{}".format(int(my_time.timestamp()),image_name)
		pic_time = str(my_time.strftime('%A %B %-d %Y %-I:%M:%S %p'))
		image_name = "{}/{}".format(image_directory,image_name)
		camera = PiCamera(resolution=(1280,720))
		sleep(10)
		camera.annotate_text = pic_time
		camera.annotate_text_size = 20
		camera.capture(image_name)
		camera.close()
		image_name = image_name.split('/')
		image_name = ['camera' if item == 'calendar_app' else item for item in image_name]
		image_name = "/".join(image_name[-3:])
		data = []
		data.append({'photo':image_name})
		data.append({'name':pic_time})
		return jsonify(data = data)
	else:
		return render_template("camera.html")

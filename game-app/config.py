from os import environ
from application.functions import get_host

class Config:
	SECRET_KEY = environ.get('SECRET_KEY')
	FLASK_ENV = environ.get('FLASK_ENV')

	STATIC_FOLDER = environ.get('STATIC_FOLDER')
	TEMPLATES_FOLDER = environ.get('TEMPLATES_FOLDER')
	IP = get_host.find_host()

from os import environ

class Config:
	SECRET_KEY = environ.get('My Key Is a Secret Farm')
	FLASK_ENV = environ.get('FLASK_ENV')

	STATIC_FOLDER = environ.get('STATIC_FOLDER')
	TEMPLATES_FOLDER = environ.get('TEMPLATES_FOLDER')

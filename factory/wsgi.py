from application import create_app

app = create_app()

if __name__ == "__main__":
	app.run()
#uwsgi --http-socket :9090 --plugins python3 --wsgi-file wsgi.py --callable app --py-autoreload

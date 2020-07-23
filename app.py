from flask import Flask
from application.route import route

app = Flask('application')
route(app)

if __name__ == '__main__':
	app.run()

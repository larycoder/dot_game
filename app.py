from flask import Flask
from dot_game.route import route

app = Flask('dot_game')
route(app)

if __name__ == '__main__':
	app.run()

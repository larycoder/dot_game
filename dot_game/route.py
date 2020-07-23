from flask import Flask

def route(app: Flask):
	@app.route("/")
	def hello():
		return "hello flask"

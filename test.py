from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dot_game/db/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "test"

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    name = db.Column(db.TEXT, nullable = False)
    age = db.Column(db.TEXT, nullable = False)

print(User.query.filter_by(id = 1).first().name)

import base64
encoded = base64.b64encode(b'hello world').decode()
decoded = base64.b64decode(encoded)

myString = "hello world"
myByte = bytes(myString, 'utf-8')
print(myByte)

import yaml
with open("install/key.yaml") as f:
    list_value = yaml.safe_load(f)


# print(list_value)
for i in list_value['guideline_list']:
    print(i['guideline']['name'])
import base64
from dot_game import app, db, bcrypt

class UserModel(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(255), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    admin = db.Column(db.Boolean, default = False, nullable = False)

    def __init__(self, name, password):
        self.name = name
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()

class GuideLineModel(db.Model):
    __tablename__ = "guideline"

    """ GuideLine Model storing guideline of game """
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    version = db.Column(db.String(255), nullable = False)
    name = db.Column(db.Text, nullable = False)
    description = db.Column(db.Text)
    code = db.Column(db.Text)

    def __init__(self, version, name, description):
        self.version = version
        self.name = name
        self.description = description
    
    def getInfo(self):
        return {
            'version': self.version,
            'name': self.name,
            'description': self.description
        }

class KeyModel(db.Model):
    __tablename__ = "keys"

    """ Key Model storing secret key for token """
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(255), nullable = True)
    key = db.Column(db.String(500), nullable = False, unique = True)
    description = db.Column(db.String(500))

    def __init__(self, name: str, key, description: str):
        self.name = name
        self.description = description
        self.key = base64.b64encode(key).decode()

    @staticmethod
    def decode64(key: str):
        """
        Decode base64 to real key
        :param str:
        :return: binary object
        """
        return base64.b64decode(key)

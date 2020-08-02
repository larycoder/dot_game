import datetime
import jwt

from dot_game.models import KeyModel

def genToken(service_name, id):
    """
    Generate the auth token
    :return: token(string)
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days = 0, minutes = 1),
            'iat': datetime.datetime.utcnow(),
            'sub': id,
            'service': service_name
        }
        return jwt.encode(
            payload,
            KeyModel.decode64(KeyModel.query.filter_by(name = service_name).first().key),
            algorithm = "HS256"
        ).decode()
    except Exception as e:
        return e

def verifyToken(service_name, token):
    """
    Decodes the auth token
    :return: payload(dict) | error(string)
    """
    try:
        payload = jwt.decode(
            token,
            KeyModel.decode64(KeyModel.query.filter_by(name = service_name).first().key)
        )
        return payload
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def regenToken(token):
    """
    Check valid token and regen new Token if the token is almost expired
    :return: error(str) | {user_id(integer), new_token(string)}
    """
    try:
        service_name = jwt.decode(token, verify = False)['service'] # get user type
    except (jwt.exceptions.InvalidTokenError, KeyError):
        return 'Invalid token. Please log in again'
    
    payload = verifyToken(service_name, token)
    if not isinstance(payload, str):
        return {
            'user_id': payload['sub'],
            'new_token': genToken(service_name, payload['sub'])
        }
    else:
        return payload
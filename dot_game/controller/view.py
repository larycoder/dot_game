from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from dot_game import db, bcrypt
from dot_game.models import UserModel, GuideLineModel

from dot_game.controller.helper import genToken, regenToken, checkAuth

core_blueprint = Blueprint('core', __name__)

class RegisterAPI(MethodView):
    """
    User Register Resource
    """
    def post(self):
        # get post data
        post_data = request.get_json()

        # check if user already exists
        user = UserModel.query.filter_by(name = post_data.get('user')).first()
        if not user:
            try:
                user = UserModel(
                    name = post_data.get('user'),
                    password = post_data.get('password')
                )
                if(user.name == "admin"):
                    user.admin = True

                # insert the user
                db.session.add(user)
                db.session.commit()

                # generate the auth token
                if(user.admin):
                    auth_token = genToken("admin", user.id)
                else:
                    auth_token = genToken("normal_user", user.id)

                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.'
            }
            return make_response(jsonify(responseObject)), 202

class LoginAPI(MethodView):
    """
    User Login Resource
    """
    
    def post(self):
        # get post data
        post_data = request.get_json()
        try:
            # fetch user
            user = UserModel.query.filter_by(name = post_data['user']).first()
            if user and bcrypt.check_password_hash(
                user.password, post_data.get('password')
            ):
                if user.admin:
                    auth_token = genToken("admin", user.id)
                else:
                    auth_token = genToken("normal_user", user.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token
                }
                return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User or password is wrong.'
                }
                return make_response(jsonify(responseObject)), 404
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again.'
            }
            return make_response(jsonify(responseObject)), 500

class GuideLineImportAPI(MethodView):
    """
    Import list of guideline
    """
    def post(self):
        post_data = request.get_json()
        resp = checkAuth(request)
        if isinstance(resp, dict):
            try:
                # add normal information
                new_guideline = GuideLineModel(
                    post_data['version'],
                    post_data['name'],
                    post_data['description']
                )
                new_guideline.user_id = resp['user_id']

                # add code of instruction if exist
                if 'code' in post_data:
                    new_guideline.code = post_data['code']

                # push to db
                db.session.add(new_guideline)
                db.session.commit()

                responseObject = {
                    'status': 'success',
                    'message': 'Successfully import instruction.',
                    'auth_token': resp['new_token']
                }
                return make_response(jsonify(responseObject)), 200
            except Exception as e:
                print(e)
                responseObject = {
                    'status': 'fail',
                    'message': 'Something wrong happend. Please try again.'
                }
                return make_response(jsonify(responseObject)), 500
        else:
            return resp

class GuideLineListAPI(MethodView):
    """
    Get list of guideline
    """
    def get(self):
        auth_header = request.headers.get('Authorization')

        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Please provide a valid token'
            }
            return make_response(jsonify(responseObject)), 401

        resp = regenToken(auth_token)
        if not isinstance(resp, str):
            new_token = resp['new_token']
            user_id = resp['user_id']
        else:
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401

        try:
            list_guideline = GuideLineModel.query.filter(db.or_(
                GuideLineModel.user_id == user_id,
                GuideLineModel.user_id == None
            )).all()
            # convert List Model to List dict
            list_dict_of_guideline = []
            for guideline in list_guideline:
                list_dict_of_guideline.append(guideline.getInfo())

            responseObject = {
                'status': 'success',
                'message': 'Successfully get guideline.',
                'guideline': list_dict_of_guideline,
                'auth_token': new_token
            }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Something wrong happend. Please try again.'
            }
            return make_response(jsonify(responseObject)), 500

# Define API view
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
guideline_list_view = GuideLineListAPI.as_view('guideline_list_api')
guideline_import_view = GuideLineImportAPI.as_view('guideline_import_api')

# Add rule for API Endpoints
core_blueprint.add_url_rule(
    '/core/register',
    view_func = registration_view,
    methods = ['POST']
)
core_blueprint.add_url_rule(
    '/core/login',
    view_func = login_view,
    methods = ['POST']
)
core_blueprint.add_url_rule(
    '/core/guideline/list',
    view_func = guideline_list_view,
    methods = ['GET']
)
core_blueprint.add_url_rule(
    '/core/guideline/import',
    view_func = guideline_import_view,
    methods = ['POST']
)
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from dot_game import db, bcrypt
from dot_game.models import UserModel, GuideLineModel

from dot_game.controller.helper import genToken, regenToken

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
                    'message': 'User does not exists.'
                }
                return make_response(jsonify(responseObject)), 404
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again.'
            }
            return make_response(jsonify(responseObject)), 500

class GuideLineAPI(MethodView):
    """
    Get list of guideline
    """
    def get(self):
        try:
            list_guideline = GuideLineModel.query.all()
            # convert List Model to List dict
            list_dict_of_guideline = []
            for guideline in list_guideline:
                list_dict_of_guideline.append(guideline.getInfo())

            responseObject = {
                'status': 'success',
                'message': 'Successfully  get guideline',
                'guideline': list_dict_of_guideline
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
guideline_view = GuideLineAPI.as_view('guideline_api')

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
    '/core/guideline',
    view_func = guideline_view,
    methods = ['GET']
)
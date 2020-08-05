# dot_game.api_doc_model

from dot_game.controller.view import api
from flask_restplus import fields

# doc model
AuthReqModel = api.model('AuthReqModel', {
    'user': fields.String(description = 'user name', required = True),
    'password': fields.String(description = 'user password', required = True)
})

ErrorResModel = api.model('ErrorResModel',{
    'status': fields.String(description = 'error status'),
    'message': fields.String(description = 'error message')
})

SuccessResModel = api.model('SuccessResModel', {
    'status': fields.String(description = 'success status'),
    'message': fields.String(description = 'success message'),
    'auth_token': fields.String(description = 'token return')
})

GuidelineListSucResModel = api.model('GuidelineListSucResModel', {
    'status': fields.String(description = 'success status'),
    'message': fields.String(description = 'success message'),
    'guideline': fields.String(description = 'list of guideline reponse'),
    'auth_token': fields.String(description = 'token return')
})

AuthHeaderReq = api.parser().add_argument('Authorization', help = 'token key', location = 'headers')
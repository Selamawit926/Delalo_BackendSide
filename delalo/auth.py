from functools import wraps
import jwt
import os
import datetime
from flask import json, Response, request, g, Blueprint
from  delalo.models import UserModel, UserSchema
from flask_restful import Api



class Auth():
  """
  Auth Class
  """
  
  @staticmethod
  def auth_required(func):
    """
    Auth decorator
    """
    @wraps(func)
    def decorated_auth(*args, **kwargs):
      if 'api-token' not in request.headers:
        return Response(
          mimetype="application/json",
          response=json.dumps({'error': 'Authentication token is not available, please login to get one'}),
          status=400
        )
      token = request.headers.get('api-token')
      data = Auth.decode_token(token)
      if data['error']:
        return Response(
          mimetype="application/json",
          response=json.dumps(data['error']),
          status=400
        )
        
      user_id = data['data']['user_id']
      check_user = UserModel.get_one_user(user_id)
      if not check_user:
        return Response(
          mimetype="application/json",
          response=json.dumps({'error': 'user does not exist, invalid token'}),
          status=400
        )
      g.user = {'id': user_id}
      return func(*args, **kwargs)
    return decorated_auth




user_api = Blueprint('user_api', __name__)
user_schema = UserSchema()

@api.route('/', methods=['POST'])
def create():
    """
    Create User Function
    """


    return custom_response({'jwt_token': token}, 201)

@user_api.route('/login', methods=['POST'])
def login():
  req_data = request.get_json()

  data, error = user_schema.load(req_data, partial=True)

  if error:
    return custom_response(error, 400)
  
  if not data.get('email') or not data.get('password'):
    return custom_response({'error': 'you need email and password to sign in'}, 400)
  
  user = UserModel.get_user_by_email(data.get('email'))

  if not user:
    return custom_response({'error': 'invalid credentials'}, 400)
  
  if not user.check_hash(data.get('password')):
    return custom_response({'error': 'invalid credentials'}, 400)
  
  ser_data = user_schema.dump(user).data
  
  token = Auth.generate_token(ser_data.get('id'))

  return custom_response({'jwt_token': token}, 200)

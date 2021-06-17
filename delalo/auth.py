from functools import wraps
from flask_jwt_extended import ( create_access_token, get_jwt ,jwt_required, get_jwt_identity)

from flask import json, Response, request, g, Blueprint
from  delalo.models import UserModel
from flask_restful import Api, Resource
from delalo.shemas import *

user_schema = UserSchema()

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        current_user = UserModel.query.filter_by(email=data['email']).first()

        if not current_user:
            return {'message': 'User with email {} doesn\'t exist'.format(data['email'])}
        
        if current_user.check_password(data['password']):
            access_token = create_access_token(identity = {'role': current_user.role, 'email': data['email']})
            return {
                'user': user_schema.dump(current_user),
                'message': f'Logged in as {current_user.firstname} {current_user.lastname}',
                'access_token': access_token
                }
        else:
            return {'message': 'Wrong credentials'}

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            db.session.add(revoked_token)
            db.session.commit()
            return {'message': 'User logout successfull'}
        except:
            return {"message": "Something went wrong"}
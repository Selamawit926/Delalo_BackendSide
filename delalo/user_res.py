from flask import request
from flask_restful import Resource, abort
from marshmallow import ValidationError
from delalo import db
from delalo.models import *
from delalo.shemas import *
from flask_jwt_extended import ( create_access_token, get_jwt, jwt_required, get_jwt_identity)

user_schema = UserSchema()
user_schemas = UserSchema(many=True)
provider_schema = ProviderSchema()

class Users(Resource):
    def post(self):
        data = request.get_json()
        try:
            args = UserSchema(partial=True).load(data)
        except ValidationError as errors:
            abort(400, message=errors.messages)
        user = UserModel(firstname=args['firstname'], 
                         lastname=args['lastname'],
                         email = args["email"],
                         password=args['password_hash'], 
                         role='user', 
                         phone=args['phone'],
                         image=args['image'],
                         address=args['address'])
        db.session.add(user)
        db.session.commit()
        access_token = create_access_token(identity = {'role': user.role, 'email': data['email']})
        return {
            'user': user_schema.dump(user),
            'message': 'User with email {} was created'.format(data['email']),
            'access_token': access_token
        }
    
    @jwt_required()
    def get(self):
        logged_user_role = get_jwt_identity()['role']
        if logged_user_role != 'admin':
            abort(400, message="This requires admin privilige")
        result = UserModel.query.all()
        return user_schemas.dump(result)   



class User(Resource):
    # @jwt_required()
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found!")

        prov_user = ProviderModel.query.filter_by(user_id=user.id).first()

        user_dump = user_schema.dump(user)
        prov_user_dump = provider_schema.dump(prov_user)

        
        return {"user_info" : user_dump,
                "prov_info" : prov_user_dump}



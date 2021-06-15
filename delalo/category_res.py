
from flask import request
from flask_restful import Resource, abort
from marshmallow import ValidationError
from delalo import db
from delalo.models import UserModel
from delalo.shemas import 


class Users(Resource):
    def post(self):
        data = request.get_json()
        try:
            args = UserSchema().load(data)
        except ValidationError as errors:
            abort(400, message=errors.messages)
        user = UserModel(firstname=args['firstname'], 
                         lastname=args['lastname'], 
                         password=args['password_hash'], 
                         role='user', 
                         phone=args['phone'],
                         image=args['image'],
                         address=args['address'])
        db.session.add(user)
        db.session.commit()
        return UserSchema().dump(user), 201

    def get(self):
        result = UserModel.query.all()
        return UserSchema(many=True).dump(result)   



class Category(Resource):
    # @jwt_required()
    def get(self, id):
        result = UserModel.query.filter_by(id=id).first()
        if not result:
            abort(404, message="User not found!")
        return UserSchema().dump(result)


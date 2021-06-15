
from flask import request
from flask_restful import Resource, abort
from marshmallow import ValidationError
from delalo import db
from delalo.models import UserModel
from delalo.shemas import UserSchema
from flask_jwt_extended import ( create_access_token, get_jwt,
                            jwt_required, get_jwt_identity)


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



class User(Resource):
    # @jwt_required()
    def get(self, id):
        result = UserModel.query.filter_by(id=id).first()
        if not result:
            abort(404, message="User not found!")
        return UserSchema().dump(result)

    # @jwt_required()
    # def patch(self, id):
    #     data = request.get_json()
    #     try:
    #         args = UserSchema(partial=True).load(data)
    #     except ValidationError as errors:
    #         abort(400, message=errors.messages)
    #     # args = cleanNullTerms(args)
    #     user_id = get_jwt_identity()
    #     if user_id == id:
    #         existing = UserModel.query.filter_by(id=id).update(args)
    #     return abort(403, message="User not authorized!")
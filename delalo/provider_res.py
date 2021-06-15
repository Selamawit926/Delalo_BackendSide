
from flask import request
from flask_restful import Resource, abort
from marshmallow import ValidationError
from marshmallow.fields import Email
from delalo import db
from delalo.models import UserModel
from delalo.shemas import *
from flask_jwt_extended import ( create_access_token, get_jwt,
                            jwt_required, get_jwt_identity)

provider_user_schema = ProviderUserSchema()
provider_schema = ProviderSchema()
user_schema = UserSchema()
provider_users_schema = ProviderUserSchema(many=True)


class Providers(Resource):
    def post(self):
        data = request.get_json()
        try:
            args = provider_user_schema.load(data)
        except ValidationError as errors:
            abort(400, message=errors.messages)
        user_prov = UserModel(firstname=args['firstname'], 
                         lastname=args['lastname'], 
                         email = args['email'],
                         password=args['password_hash'], 
                         role='provider', 
                         phone=args['phone'],
                         image=args['image'],
                         address=args['address'])

        provider = ProviderModel(description=args['description'],
                                 category=args['category'],
                                 jobs_done=args['jobs_done'],
                                 per_hour_wage=args['per_hour_wage'],
                                 recommendation=args['recommendation'],
                                 average_rating=args['average_rating'],
                                 user=user_prov)                 
        db.session.add(provider)
        db.session.commit()
        return provider_user_schema.dump(data)

    # def get(self):
    #     prov = ProviderModel.query.all()
    #     prov_user = UserModel.query.all()

    #     for item

    #     return  



class Provider(Resource):
    # @jwt_required()
    def get(self, id):
        prov = ProviderModel.query.filter_by(id=id).first()
        prov_user = UserModel.query.filter_by(id=prov.user_id).first()
        if not prov_user:
            abort(404, message="Provider not found!")

        prov_dump = provider_schema.dump(prov)
        prov_user_dump = user_schema.dump(prov_user)

        
        return {"user_info" : prov_user_dump,
                "prov_info" : prov_dump}

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
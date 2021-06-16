
from flask import request
from flask_restful import Resource, abort
from marshmallow import ValidationError
from delalo import db
from delalo.models import UserModel,ReviewModel
from delalo.shemas import OrderSchema, UserSchema,ReviewSchema
from flask_jwt_extended import ( create_access_token, get_jwt,
                            jwt_required, get_jwt_identity)

reviewschema=ReviewSchema()
reviewschemas=ReviewSchema(many=True)

class Reviews(Resource):
    def post(self):
        data = request.get_json()
        try:
            args = ReviewSchema(partial=True).load(data)
        except ValidationError as errors:
            abort(400, message=errors.messages)

        review=ReviewModel(rating=args["rating"],
                            comment=args["comment"],
                            order_id=args["order_id"])

        db.session.add(review)
        db.session.commit()
        return reviewschema.dump(review), 201
    
    def get(self):
        result=ReviewModel.query.all()
        return reviewschemas.dump(result)

class Review(Resource):
    def get(self,id):
        result=ReviewModel.query.filter_by(order_id=id).first()
        return reviewschema.dump(result)




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
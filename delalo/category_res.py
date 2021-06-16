
from os import name
import re
from delalo.shemas import CategorySchema
from flask import jsonify, request
from flask_restful import Resource, abort
from marshmallow import ValidationError
from delalo import db
from delalo.models import UserModel
from delalo.models import CategoryModel

from marshmallow.fields import Email
from delalo.common.util import cleanNullTerms
from flask_jwt_extended import ( create_access_token, get_jwt,
                            jwt_required, get_jwt_identity)

category_schema = CategorySchema()
category_schema = CategorySchema(many=True)


class Categories(Resource):
    # @jwt_required()
    def get(self):
        categories = CategoryModel.query.all() 
        cat_list = []
        for category_e in categories:
            cat_dict={
                "id" : category_e.id,
                "name": category_e.name,
                "image": category_e.image,
                "num_of_providers":category_e.num_of_providers,
                "description":category_e.description

            }
            cat_list.append(cat_dict)
        if list:
            return jsonify(cat_list)
        abort(404, message="No Ctegories in the database")    
    def post(self):
        category_data = request.get_json()
        if not category_data:
            return {'message': 'No input data provided'}
        
        try:
            cat_args= CategorySchema(partial=True).load(category_data)
        except ValidationError as errors:
            abort(400, message=errors.messages)
        # if errors:
        #     return errors, 422
        category_info = CategoryModel.query.filter_by(name=cat_args['name']).first()
        if category_info:
             return {'message': 'Category already exists'}, 400
        category_info = CategoryModel(
            name=cat_args['name'],
            image=cat_args['image'],
            num_of_providers=cat_args['num_of_providers'],
            description=cat_args['description']
        )
        
        # return result
        # if result == None:
           
        db.session.add(category_info)
        db.session.commit()
        return CategorySchema().dump(category_info)

        # return abort(message="Category exists")

        # if not result:
        #     abort(404, message="User not found!")
        # return UserSchema().dump(result)

class Category(Resource):
    def get(self, id):

        cat_by_id = CategoryModel.query.filter_by(id=id).first()
        if not cat_by_id:
            abort(404, message="Catagory not found!")
        category_dump=category_schema.dump(cat_by_id)
        return {"category":category_dump}
    def delete(self, id):
        # category_data = request.get_json()
        # if not category_data:
        #     return {'message': 'No input data provided'}
        # data = category_schema.load(category_data)
        cat_by_id = CategoryModel.query.filter_by(id=id).first()
        if cat_by_id:
            CategoryModel.query.filter_by(id=id).delete()
            db.session.commit()
            return {'message': ' Category deleted'}
        return {'message': ' Category does not exist'}
        
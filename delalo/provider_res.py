
from flask import jsonify, request
from flask_restful import Resource, abort
from marshmallow import ValidationError
from marshmallow.fields import Email
from delalo import db
from delalo.models import UserModel
from delalo.shemas import *
from delalo.common.util import cleanNullTerms
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
    #     provs = ProviderModel.query.all()

    #     lst = []
    #     for item in provs:
    #         user = UserModel.query.filter_by(id=item.user_id).first()
    #         diction = {
    #             "id" : user.id,
    #             "firstname" : user.firstname,
    #             "lastname" : user.lastname,
    #             "email" : user.email,
    #             "role" : user.role,
    #             "phone" : user.phone,
    #             "image" : user.image,
    #             "address" : user.address,
    #             "provider_id" : item.id,
    #             "description" : item.description,
    #             "category" : item.category,
    #             "jobs_done" : item.jobs_done,
    #             "per_hour_wage" : item.per_hour_wage,
    #             "recommendation" : item.recommendation,
    #             "average_rating" : float(item.average_rating)
    #         }

    #         lst.append(diction)

    #     if list:
    #         return jsonify(results=lst)
    #     abort(404, message="No providers in the database") 


    def get(self, category_id):
        name = CategoryModel.query.filter_by(id=category_id).first().name
        # capitalize
        provs = ProviderModel.query.filter_by(category=name).all()

        lst = []
        for item in provs:
            user = UserModel.query.filter_by(id=item.user_id).first()
            diction = {
                "id" : user.id,
                "firstname" : user.firstname,
                "lastname" : user.lastname,
                "email" : user.email,
                "role" : user.role,
                "phone" : user.phone,
                "image" : user.image,
                "address" : user.address,
                "provider_id" : item.id,
                "description" : item.description,
                "category" : item.category,
                "jobs_done" : item.jobs_done,
                "per_hour_wage" : item.per_hour_wage,
                "recommendation" : item.recommendation,
                "average_rating" : float(item.average_rating)
            }

            lst.append(diction)

        if list:
            return jsonify(results=lst)
        abort(404, message=f"No providers in the database with category id:{category_id}")          

        
class Provider(Resource):
    def get(self, id):
        prov = ProviderModel.query.filter_by(id=id).first()
        prov_user = UserModel.query.filter_by(id=prov.user_id).first()
        if not prov_user:
            abort(404, message="Provider not found!")

        prov_dump = provider_schema.dump(prov)
        prov_user_dump = user_schema.dump(prov_user)

        
        return {"user_info" : prov_user_dump,
                "prov_info" : prov_dump}

    def patch(self, id):
        data = request.get_json()
        try:
            args = ProviderSchema(partial=True).load(data)
        except ValidationError as errors:
            abort(400, message=errors.messages)
        args = cleanNullTerms(args)
        
        
        provider = ProviderModel.query.filter_by(id=id).first()
        if provider:
            provider.jobs_done += 1
            db.session.commit() 
            # if bool(args['average_rating']):
            try:
                rating = args['average_rating']
                prov_review_count = OrderModel.query.filter_by(provider_id=provider.id).count()
                prov_review_count = float(prov_review_count)
                old_average_rating = provider.average_rating
                old_average_rating = float(old_average_rating)
                sum = old_average_rating * prov_review_count
                sum+=rating
                new_average_rating = sum/(prov_review_count + 1)
                provider.average_rating = new_average_rating
                db.session.commit()
            except:
                abort(400, message="New Rating missing")
            provider = ProviderModel.query.filter_by(id=id).first()
            if provider:
                return provider_schema.dump(provider)

        abort(404, message="provider not found!")    




class TopProviders(Resource):
    def get(self):
        provs = ProviderModel.query.order_by(ProviderModel.average_rating.desc()).limit(6).all()

        lst = []
        for item in provs:
            user = UserModel.query.filter_by(id=item.user_id).first()
            diction = {
                "id" : user.id,
                "firstname" : user.firstname,
                "lastname" : user.lastname,
                "email" : user.email,
                "role" : user.role,
                "phone" : user.phone,
                "image" : user.image,
                "address" : user.address,
                "provider_id" : item.id,
                "description" : item.description,
                "category" : item.category,
                "jobs_done" : item.jobs_done,
                "per_hour_wage" : item.per_hour_wage,
                "recommendation" : item.recommendation,
                "average_rating" : float(item.average_rating)
            }

            lst.append(diction)

        if list:
            return jsonify(results=lst)
        abort(404, message="No providers in the database") 

class TopCategoryProviders(Resource):
    def get(self, category_id):
        name = CategoryModel.query.filter_by(id=category_id).first().name
        # capitalize
        provs = ProviderModel.query.filter_by(category=name).order_by(ProviderModel.average_rating.desc()).limit(3).all()

        lst = []
        for item in provs:
            user = UserModel.query.filter_by(id=item.user_id).first()
            diction = {
                "id" : user.id,
                "firstname" : user.firstname,
                "lastname" : user.lastname,
                "email" : user.email,
                "role" : user.role,
                "phone" : user.phone,
                "image" : user.image,
                "address" : user.address,
                "provider_id" : item.id,
                "description" : item.description,
                "category" : item.category,
                "jobs_done" : item.jobs_done,
                "per_hour_wage" : item.per_hour_wage,
                "recommendation" : item.recommendation,
                "average_rating" : float(item.average_rating)
            }

            lst.append(diction)

        if list:
            return jsonify(results=lst)
        abort(404, message="No providers in the database")     
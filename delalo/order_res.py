
import datetime

from flask.json import jsonify
from delalo.user_res import User
import random
from typing_extensions import ParamSpecArgs
from flask import request
from flask_restful import Resource, abort
from marshmallow import ValidationError
from marshmallow.fields import DateTime
from delalo import db
from delalo.models import *
from delalo.shemas import *
from flask_jwt_extended import ( create_access_token, get_jwt,
                            jwt_required, get_jwt_identity)


orderSchema= OrderSchema()
orderSchemas=OrderSchema(many=True)
user_schema= UserSchema()
provider_schema =ProviderSchema() 
review_schema = ReviewSchema()

class Orders(Resource):
    def post(self):
        seeker_id=request.args.get("seeker_id")
        provider_id=request.args.get("provider_id")
        order= OrderModel(status="pending",
                            is_completed=False,
                            order_created_date=str(datetime.datetime
                            .now()),
                            order_completed_date="none",
                            start_time=datetime.datetime.now(),
                            saved_time=0,
                            unique_code=random.randint(1000,9000),
                            seeker_id=seeker_id,
                            provider_id=provider_id,
                            )

        db.session.add(order)
        db.session.commit()
        return orderSchema.dump(order), 201

    def get(self):
        results= OrderModel.query.all()
        objs=[]
        for result in results:
            
            user=UserModel.query.filter_by(id=result.seeker_id).first()
            provider=ProviderModel.query.filter_by(id=result.provider_id).first()
            provider_user = UserModel.query.filter_by(id=provider.user_id).first()
            review=ReviewModel.query.filter_by(order_id=result.id).first()
            objs.append({
                "user": user_schema.dump(user),
                "provider" : {
                    "user_info": user_schema.dump(provider_user),
                    "provider_info": provider_schema.dump(provider)
                },
                "review" : review_schema.dump(review),
                "order": orderSchema.dump(result)
            })
        
           
        return jsonify(results=objs)



class OrderStatus(Resource):
    
    # def __init__(self) -> None:
    #     previous=0
    #     totaltime=0
    #     starthour=0
    #     pausedhour=0

    def put(self,id):
        status= request.args.get("status")
        progress=request.args.get("progress")
        result=OrderModel.query.filter_by(id=id).first()
        # return orderSchema.dump(result)
        # return orderSchema.dump(result)
        if status=="accepted":
            result.status="active"
            db.session.commit()

        elif status=="declined":
            result.status="declined"
            db.session.commit()

        # return OrderModel.query.filter_by(id=id).first()
        if progress=="started":
            now=datetime.datetime.now()
            result.start_time=now
            result.progress="started"
            db.session.commit()
            
        elif progress=="paused":
            now=datetime.datetime.now()
            diff=now-result.start_time
            hours=diff.total_seconds()/3600
            result.saved_time= float(result.saved_time)+float(hours)
            result.progress="paused"
            db.session.commit()

        elif progress=="finished":
            prov=ProviderModel.query.filter_by(id=result.provider_id).first()
            now=datetime.datetime.now()
            diff=now-result.start_time
            hours=diff.total_seconds()/3600
            result.saved_time=float(result.saved_time)+float(hours)
            payment=result.saved_time*prov.per_hour_wage
            result.final_payment=payment
            result.progress="finished"
            result.is_completed=True
            db.session.commit()

class Order(Resource):
    def get(self,id):
        results=OrderModel.query.filter_by(seeker_id=id).all()
        if not results:
            abort(404, message="Order not found!")

        objs=[]
        for result in results:
            user=UserModel.query.filter_by(id=result.seeker_id).first()
            provider=ProviderModel.query.filter_by(id=result.provider_id).first()
            provider_user = UserModel.query.filter_by(id=provider.user_id).first()
            review=ReviewModel.query.filter_by(order_id=result.id).first()

            objs.append({
                "user": user_schema.dump(user),
                "provider" : {
                    "user_info": user_schema.dump(provider_user),
                    "provider_info": provider_schema.dump(provider)
                },
                "review" : review_schema.dump(review),
                "order": orderSchema.dump(result)
            })
        
           
        return jsonify(results=objs)
        # return orderSchemas.dump(result)
class Jobs(Resource):
    def get(self,id):
        results=OrderModel.query.filter_by(provider_id=id).all()
        if not results:
            abort(404, message="Jobs not found!")
        objs=[]
        for result in results:
            user=UserModel.query.filter_by(id=result.seeker_id).first()
            provider=ProviderModel.query.filter_by(id=result.provider_id).first()
            provider_user = UserModel.query.filter_by(id=provider.user_id).first()
            review=ReviewModel.query.filter_by(order_id=result.id).first()

            objs.append({
                "user": user_schema.dump(user),
                "provider" : {
                    "user_info": user_schema.dump(provider_user),
                    "provider_info": provider_schema.dump(provider)
                },
                "review" : review_schema.dump(review),
                "order": orderSchema.dump(result)
            })
        
           
        return jsonify(results=objs)
        # return orderSchemas.dump(result)
class DeleteOrder(Resource):
    def delete(self,id):
        result=OrderModel.query.filter_by(id=id).first()
        if not result:
            abort(404, message="Order not found!")
        
        OrderModel.query.filter_by(id=id).delete()
        # db.session.remove(result)
        db.session.commit()

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
import re
from marshmallow import fields, validates, ValidationError
from sqlalchemy.orm import load_only
from delalo import ma
from delalo import models
from delalo.models import *


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "firstname", "lastname", "email", "password_hash", "role", "phone", "image", "address")
        model = UserModel
        ordered = True
    
    firstname = fields.String(required=True)
    lastname = fields.String(required=True)
    email = fields.String(required=True)
    password_hash = fields.String(load_only=True)
    role = fields.String(required=False)
    phone = fields.String(required=True)
    image = fields.String(required=False)
    address = fields.String(required=True)


    # @validates("phone")
    # def validate_mobile(self, value):
    #     rule_phone = re.compile(r'^\+(?:[0-9]●?){6,14}[0-9]$')

    #     if not rule_phone.search(value):
    #         msg = u"Invalid mobile number."
    #         raise ValidationError(msg)

    @validates("email")
    def validate_email(self, email):
        rule_email = re.compile(r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$')

        if not rule_email.search(email):
            msg = u"Invalid email address."
            raise ValidationError(msg)

        if bool(UserModel.query.filter_by(email=email).first()):
            raise ValidationError(
                'username with email - "{email}" already exists, '
                'please use a different email.'.format(email=email)
            )

class ProviderSchema(ma.Schema):
    class Meta:
        fields = ("id", "description", "category", "jobs_done", "per_hour_wage", "recommendation", "average_rating", "user_id")
        model = ProviderModel
        ordered = True

    description = fields.String(required=True)
    category = fields.String(required=True)
    jobs_done = fields.Integer(required=True)  
    per_hour_wage = fields.Integer(required=True)
    recommendation = fields.String(required=True)
    average_rating = fields.Float(required=False)
    user_id = fields.Integer(required=True)

class CategorySchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "image","num_of_providers", "description")
        model = CategoryModel
        ordered = True

    name = fields.String(required=True) 
    image = fields.String(required=False) 
    num_of_providers = fields.Integer(required=True)
    description = fields.String(required=True)


class ReviewSchema(ma.Schema):
    class Meta:
        fields = ("id", "rating", "comment", "order_id")                    
        model = OrderModel
        ordered = True

    rating = fields.Integer(required=True)
    comment = fields.String(required=True)
    order_id = fields.Integer(required=True)


class OrderSchema(ma.Schema):
    class Meta:
        fields = ("id", "status", "progress", "is_completed", "order_created_date", "order_completed_date", "start_time", "saved_time", "unique_code", "seeker_id", "provider_id")
        model = OrderModel
        ordered = True

    status = fields.String(required=True)
    progress = fields.String(required=False)
    is_completed = fields.Boolean(required=True)
    order_created_date = fields.String(required=True)
    order_completed_date = fields.String(required=False)
    start_time = fields.DateTime(required=True)
    saved_time = fields.Float(required=True)
    unique_code = fields.Float(required=True)
    seeker_id = fields.Integer(required=True)
    provider_id = fields.Integer(required=True)




class ProviderUserSchema(ma.Schema):
    class Meta:
        fields = ("id", "firstname", "lastname", "email", "password_hash", "role", "phone", "image", "address","Provider_id", "description", "category", "jobs_done", "per_hour_wage", "recommendation", "average_rating")    
        ordered = True
    id = fields.Integer(dump_only=True)
    firstname = fields.String(required=True)
    lastname = fields.String(required=True)
    email = fields.String(required=True)
    password_hash = fields.String(load_only=True, data_key="password")
    role = fields.String(required=False)
    phone = fields.String(required=True)
    image = fields.String(required=False)
    address = fields.String(required=True)  
    description = fields.String(required=True)
    category = fields.String(required=True)
    jobs_done = fields.Integer(required=True)  
    per_hour_wage = fields.Integer(required=True)
    recommendation = fields.String(required=True)
    average_rating = fields.Float(required=True)
    user_id = fields.Integer(dump_only=True)  
    

    @validates("email")
    def validate_email(self, email):
        rule_email = re.compile(r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$')

        if not rule_email.search(email):
            msg = u"Invalid email address."
            raise ValidationError(msg)

        if bool(UserModel.query.filter_by(email=email).first()):
            raise ValidationError(
                'username with email - "{email}" already exists, '
                'please use a different email.'.format(email=email)
            )
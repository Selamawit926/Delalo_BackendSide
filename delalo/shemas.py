import re
from marshmallow import fields, validates, ValidationError
from delalo import ma
from delalo import models
from delalo.models import *


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "firstname", "lastname", "email", "password", "role", "phone", "image", "address")
        model = UserModel
        ordered = True
    
    firstname = fields.String(required=True)
    lastname = fields.String(required=True)
    email = fields.String(required=True)
    # password_hashed = fields.String(load_only=True, data_key="password")
    # role = fields.String(required=True)
    phone = fields.String(required=True)
    image = fields.String(required=False)
    address = fields.String(required=True)


    @validates("phone")
    def validate_mobile(self, value):
        rule_phone = re.compile(r'^\+(?:[0-9]●?){6,14}[0-9]$')

        if not rule_phone.search(value):
            msg = u"Invalid mobile number."
            raise ValidationError(msg)

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



class CategorySchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "num_of_providers", "description")
        model = CategoryModel
        ordered = True
        
                    
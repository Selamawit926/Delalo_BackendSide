from datetime import datetime
from enum import unique

from sqlalchemy.orm import joinedload, lazyload
from delalo import db, bcrypt





class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(80), nullable=True)
    address = db.Column(db.String(50), nullable=False)

    provider = db.relationship('ProviderModel', back_populates='user', uselist=False, lazy=False)
    orders = db.relationship('OrderModel', back_populates='user')

    @property
    def password(self):
        raise AttributeError('password: write-only field')
    
    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)



class ProviderModel(db.Model):
    __tablename__ = "provider"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(70), nullable=False)
    jobs_done = db.Column(db.Integer, nullable=False)
    per_hour_wage = db.Column(db.Integer, nullable=False)
    recommendation = db.Column(db.String, nullable=False)
    average_rating = db.Column(db.Numeric(10,2), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)

    user = db.relationship('UserModel', back_populates='provider')
    orders = db.relationship('OrderModel', back_populates='provider') 


class OrderModel(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(70), nullable=False)
    progress = db.Column(db.String(10), nullable=True)
    is_completed = db.Column(db.Boolean)
    order_created_date = db.Column(db.String(30))
    order_completed_date = db.Column(db.String(30))
    start_time = db.Column(db.DateTime)
    saved_time = db.Column(db.Numeric)
    unique_code = db.Column(db.Integer)

    seeker_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)

    user = db.relationship('UserModel', back_populates='orders')
    provider = db.relationship('ProviderModel', back_populates='orders')

    
    review = db.relationship('ReviewModel', back_populates='order', uselist=False)




class ReviewModel(db.Model):
    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key=True)    
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)

    order = db.relationship('OrderModel', back_populates='review', lazy=False)



class CategoryModel(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    num_of_providers = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)











import os 

class Config:
    SECRET_KEY = '81f3d659737f288fe3f74f69d878a652'
    JWT_SECRET_KEY = '81f3d659737f288fe3f74f69d878a652'
    JWT_BLACKLIST_ENABLED = ['access']
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:superuser@localhost:5432/delalodb'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
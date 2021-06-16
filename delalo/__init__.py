from delalo.common.config import Config
from flask import Flask, Blueprint, json
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS


app = Flask(__name__)
api_bp = Blueprint('api', __name__)
app.config.from_object(Config)
api = Api(api_bp)

# jwt = JWTManager(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
cors = CORS(app)



from delalo.user_res import User,Users
api.add_resource(Users, '/users')
api.add_resource(User, '/users/<int:id>') 
from delalo.category_res import Category,Categories
api.add_resource(Categories, '/categories')
api.add_resource(Category, '/categories/<int:id>') 


app.register_blueprint(api_bp, url_prefix='/delalo')
   

@app.errorhandler(500)
@app.errorhandler(404)
@app.errorhandler(403)
def error_handler(e):
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

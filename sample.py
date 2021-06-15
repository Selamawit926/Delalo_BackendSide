from delalo.shemas import *
from delalo import create_app
from flask import jsonify
from delalo import db, ma
from delalo.models import UserModel



# app = create_app()
# # # uncomment the following 2 lines, if database doesn't exist.
# # with app.app_context():
# #     db.create_all() 
# app.app_context().push()   


# @app.route("/")
# def hello_world():
#     to_be_dumped = UserModel.query.filter_by(firstname="Biniyam").first()
#     print(to_be_dumped.firstname)
#     data = UserSchema().dump(to_be_dumped)
#     return data

    
# if __name__ == '__main__':
#     app.run(host='localhost', port=51044, debug=True)
# user = UserModel(firstname = "Biniyam",
#                  lastname = "Abiy",
#                  email = "bini@gmail.com",
#                  password = "12345678",
#                  role = "admin",
#                  phone = "0934982934",
#                  image = "./img/56.jpg",
#                  address = "Addis")

# db.session.add(user)
# db.session.commit()


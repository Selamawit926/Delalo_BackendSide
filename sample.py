from delalo.category_res import Category
from delalo.shemas import *
from delalo import app
from flask import jsonify
from delalo import db, ma
from delalo.models import UserModel
import datetime



# user6 = UserModel(firstname = "Bini",
#                  lastname = "Abiy",
#                  email = "biniy@gmail.com",
#                  password = "12345678",
#                  role = "provider",
#                  phone = "0934982934",
#                  image = "./img/56.jpg",
#                  address = "Addis")

# provider6 = ProviderModel(
#     description = "This is biniyam",
#     category = "Delivery",
#     jobs_done = 0,
#     per_hour_wage = 0,
#     recommendation = "/recommendation",
#     average_rating = 0,
#     user=user6
# )


# user7 = UserModel(firstname = "sel",
#                  lastname = "elias",
#                  email = "sel@gmail.com",
#                  password = "12345678",
#                  role = "provider",
#                  phone = "0934982934",
#                  image = "./img/56.jpg",
#                  address = "Addis")
# provider7 = ProviderModel(
#     description = "This is selam",
#     category = "Tutor",
#     jobs_done = 2,
#     per_hour_wage = 35,
#     recommendation = "/recommendation",
#     average_rating = 0,
#     user=user7
# )



# user8 = UserModel(firstname = "Amly",
#                  lastname = "Ge",
#                  email = "amly@gmail.com",
#                  password = "12345678",
#                  role = "provider",
#                  phone = "0934982934",
#                  image = "./img/56.jpg",
#                  address = "Addis")
# provider8 = ProviderModel(
#     description = "This is Amly",
#     category = "Electrcian",
#     jobs_done = 1,
#     per_hour_wage = 56,
#     recommendation = "/recommendation",
#     average_rating = 0,
#     user=user8
# )
# user9 = UserModel(firstname = "Ayda",
#                  lastname = "sultan",
#                  email = "Ayda@gmail.com",
#                  password = "12345678",
#                  role = "provider",
#                  phone = "0934982934",
#                  image = "./img/56.jpg",
#                  address = "Addis")
# provider9 = ProviderModel(
#     description = "This is Ayda",
#     category = "Mechanic",
#     jobs_done = 2,
#     per_hour_wage = 20,
#     recommendation = "/recommendation",
#     average_rating = 1,
#     user=user9
# )
# user10 = UserModel(firstname = "Semere",
#                  lastname = "Seme",
#                  email = "semere@gmail.com",
#                  password = "12345678",
#                  role = "provider",
#                  phone = "0934982934",
#                  image = "./img/56.jpg",
#                  address = "Addis")
# provider10 = ProviderModel(
#     description = "This is Semere",
#     category = "Delivery",
#     jobs_done = 0,
#     per_hour_wage = 0,
#     recommendation = "/recommendation",
#     average_rating = 0,
#     user=user10
# )

# user1 = UserModel(firstname = "Biniyam",
#                  lastname = "Abiy",
#                  email = "binii@gmail.com",
#                  password = "12345678",
#                  role = "admin",
#                  phone = "0934982934",
#                  image = "./img/56.jpg",
#                  address = "Addis")

# user2 = UserModel(firstname = "Amsale",
#                  lastname = "G/hana",
#                  email = "amlyy@gmail.com",
#                  password = "12345678",
#                  role = "admin",
#                  phone = "0934982934",
#                  image = "./img/56.jpg",
#                  address = "Addis")

# user3 = UserModel(firstname = "Sitota",
#                  lastname = "Ezra",
#                  email = "easy@gmail.com",
#                  password = "12345678",
#                  role = "admin",
#                  phone = "0934982934",
#                  image = "./img/56.jpg",
#                  address = "Addis")


# user4 = UserModel(firstname = "Ayda",
#                  lastname = "Sultan",
#                  email = "ashos@gmail.com",
#                  password = "12345678",
#                  role = "admin",
#                  phone = "0934982934",
#                  image = "./img/56.jpg",
#                  address = "Addis")

# user5 = UserModel(firstname = "Selamawit",
#                  lastname = "Elias",
#                  email = "selamm@gmail.com",
#                  password = "12345678",
#                  role = "admin",
#                  phone = "0934982934",
#                  image = "./img/56.jpg",
#                  address = "Addis")
                 

# category1= CategoryModel(name="Delivery",
#                         num_of_providers=0,
#                         description="Fast delivery")

# category2= CategoryModel(name="Cleaning",
#                         num_of_providers=0,
#                         description="Fast cleaning")
                        
# category3= CategoryModel(name="Electrician",
#                         num_of_providers=0,
#                         description="Fast electricity")


# category4= CategoryModel(name="Construction",
#                         num_of_providers=0,
#                         description="Fast construction")

# category5= CategoryModel(name="Mechanic",
#                         num_of_providers=0,
#                         description="Mechanic work")
                        
# category6= CategoryModel(name="Tutor",
#                         num_of_providers=0,
#                         description="Great tutor")
# category1= CategoryModel(name="Delivery",
#                         image = "./img/56.jpg",
#                         num_of_providers=0,
                       
#                         description="Fast delivery")

# category2= CategoryModel(name="Cleaning",
#                         num_of_providers=0,
#                         image = "./img/56.jpg",
#                         description="Fast cleaning")
                        
# category3= CategoryModel(name="Electrician",
#                         image = "./img/56.jpg",
#                         num_of_providers=0,
#                         description="Fast electricity")


# category4= CategoryModel(name="Construction",
#                         image = "./img/56.jpg",
#                         num_of_providers=0,
#                         description="Fast construction")

# category5= CategoryModel(name="Mechanic",
#                         image = "./img/56.jpg",
#                         num_of_providers=0,
#                         description="Mechanic work")
                        
# category6= CategoryModel(name="Tutor",
#                         image = "./img/56.jpg",
#                         num_of_providers=0,
#                         description="Great tutor")


# order1 = OrderModel(
#     status = "pending",
#     is_completed = False,
#     order_created_date = "05-05-2021",
#     order_completed_date = "05-05-2021",
#     start_time = datetime.datetime.now(),
#     saved_time = 1.6,
#     unique_code = 4040,
#     seeker_id = 7,
#     provider_id = 4
# )                        


# order2 = OrderModel(
#     status = "pending",
#     is_completed = False,
#     order_created_date = "05-05-2021",
#     order_completed_date = "05-05-2021",
#     start_time = datetime.datetime.now(),
#     saved_time = 1.6,
#     unique_code = 4040,
#     seeker_id = 7,
#     provider_id = 3
# ) 


# order3 = OrderModel(
#     status = "pending",
#     is_completed = False,
#     order_created_date = "05-05-2021",
#     order_completed_date = "05-05-2021",
#     start_time = datetime.datetime.now(),
#     saved_time = 1.6,
#     unique_code = 4040,
#     seeker_id = 2,
#     provider_id = 4
# ) 

# review1 = ReviewModel(
#     rating = 4,
#     comment = "Wunderbar",
#     order_id = 1
# )             

# db.session.add(user1)
# db.session.add(user2)
# db.session.add(user3)
# db.session.add(user4)
# db.session.add(user5)
# db.session.add(provider6)
# db.session.add(provider7)
# db.session.add(provider8)
# db.session.add(provider9)
# db.session.add(provider10)
# db.session.add(category1)
# db.session.add(category2)
# db.session.add(category3)
# db.session.add(category4)
# db.session.add(category5)
# db.session.add(category6)
# db.session.add(order1)
# db.session.add(order2)
# db.session.add(order3)
# db.session.add(review1)

db.session.commit()


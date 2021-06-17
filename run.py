from delalo import app, db
#uncomment the following line if the database doesn't exit
# db.create_all()


if __name__ == '__main__':
    app.run(host='localhost', port=51044, debug=True)
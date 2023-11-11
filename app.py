from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from model import db, Users, Role
from flask_restful import Api
from api import Generate, Templates, Circulars, Login
from configure import DevelopmentConfig

# from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.sqlite3'
app.config.from_object(DevelopmentConfig)
db.init_app(app)
datastore = SQLAlchemyUserDatastore(db, Users, Role)
app.security = Security(app,datastore)
app.app_context().push()
API = Api(app)

# ------------------------------------------------------------
# DO NOT DELETE - HARSHITA
# ------------------------------------------------------------
# bcrypt = Bcrypt(app)
# @app.route('/test')
# def test():
#     x = "Hello"
#     hashed = bcrypt.generate_password_hash(x)
#     check = "Hello"
#     hashed_check = bcrypt.check_password_hash(hashed, check)
#     return str(hashed_check)
# -------------------------------------------------------------

API.add_resource(Generate, '/generate')
API.add_resource(Templates, '/templates')
API.add_resource(Circulars, '/circular')
API.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(debug=True)

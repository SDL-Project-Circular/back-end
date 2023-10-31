from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from model import db
from flask_restful import Api
from api import Generate, Templates, Circular

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.sqlite3'
db.init_app(app)
app.app_context().push()
API = Api(app)


API.add_resource(Generate, '/generate')
API.add_resource(Templates, '/templates')
API.add_resource(Circular, '/circular')

if __name__ == '__main__':
    app.run(debug=True)

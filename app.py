from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from model import db, Content
from flask_restful import Api
from api import Generate, Templates

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.sqlite3'
db.init_app(app)
app.app_context().push()
API = Api(app)


@app.route("/")
def trial_function():
    return render_template('index.html')


@app.route("/fetch")
def read():
    return render_template('view.html')


API.add_resource(Generate, '/generate')
API.add_resource(Templates, '/templates')

if __name__ == '__main__':
    app.run(debug=True)

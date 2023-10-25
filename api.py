import errno
import sqlite3
from datetime import datetime

import sqlalchemy
from flask import request, jsonify, redirect
from flask_restful import Resource
from model import *


class Generate(Resource):
    def post(self):
        try:
            data = request.form.to_dict() or request.json
            data_list = list(data.values())
            date_object = datetime.strptime(data_list[0], '%Y-%m-%d').date()
            temp = Template(template_name="Soloman")
            db.session.add(temp)
            db.session.commit()
            x = db.session.query(Template).filter_by(template_name="Soloman").first().template_id
            data_object = Content(template_id=int(x), ref_no=data_list[1], from_address=data_list[2],
                                  to_address=data_list[3], subject=data_list[4], body=data_list[5],
                                  sign_off=data_list[6], copy_to=data_list[7], date=date_object)
            db.session.add(data_object)
            db.session.commit()
            temp_id = Template.query.filter_by(template_name="Soloman").first().template_id
            return {
                "status": "Success",
                "id": temp_id
            }
        except Exception as e:
            print(e)
            return {"status": "Failed"}

    def get(self):
        try:
            template_id = request.args.get('id')
            if template_id:
                data = Content.query.filter_by(template_id=template_id).all()
            else:
                data = Content.query.all()
            if data:
                return jsonify(data)
        except:
            return {"status": "Failed"}, 500


class Templates(Resource):
    def get(self):
        data = Template.query.all()
        if data:
            return jsonify(data)

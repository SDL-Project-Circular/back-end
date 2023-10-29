import errno
import sqlite3
from datetime import datetime

import sqlalchemy.exc
from flask import request, jsonify, redirect
from flask_restful import Resource
from model import *


class Generate(Resource):
    def post(self):
        data = request.form.to_dict() or request.json
        data_list = list(data.values())
        date_object = datetime.strptime(data_list[0], '%Y-%m-%d').date()
        temp = Template(template_name=data_list[8])
        try:
            db.session.add(temp)
            db.session.commit()
        except:
            return {"status": "failed"}
        try:
            data_object = Content(template_id=int(temp.template_id), ref_no=data_list[1], from_address=data_list[2],
                                  to_address=data_list[3], subject=data_list[4], body=data_list[5],
                                  sign_off=data_list[6], copy_to=data_list[7], date=date_object)
            db.session.add(data_object)
            db.session.commit()
            return {
                "status": "success",
                "id": temp.template_id
            }
        except sqlalchemy.exc.IntegrityError:
            return {"status": "failed"}
        except Exception as e:
            print(e)
            return {"status": "failed"}

    def get(self):
        try:
            template_id = request.args.get('id')
            if template_id:
                data = Content.query.filter_by(template_id=template_id).first()
            else:
                data = Content.query.all()
            print(data)
            if data:
                return jsonify(data)
            else:
                return {"status": "no"}
        except:
            return {"status": "failed"}, 500

    def delete(self):
        try:
            template_id = request.args.get('id')
            if template_id:
                data = Content.query.filter_by(template_id=template_id).first()
                content = Template.query.filter_by(template_id=template_id).first()
                db.session.delete(content)
                db.session.commit()
                db.session.delete(data)
                db.session.commit()
                return {"status": "success"}
        except:
            return {"status": "failed"}


class Templates(Resource):
    def get(self):
        ref_name = request.args.get("ref_no")
        if ref_name:
            data = Content.query.filter_by(ref_no=ref_name).first()
            if data:
                return {"status": True}
            else:
                return {"status": False}
        data = Template.query.all()
        if data:
            return jsonify(data)
        else:
            return {"status": "no"}

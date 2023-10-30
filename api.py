from datetime import datetime

import sqlalchemy.exc
from flask import request, jsonify
from flask_restful import Resource
from model import *


class Generate(Resource):
    def post(self):
        data = request.form.to_dict() or request.json
        data_list = list(data.values())
        # print(data_list)
        date_object = datetime.strptime(data_list[0], '%Y-%m-%d').date()
        temp = Template(template_name=data_list[8])
        try:
            db.session.add(temp)
            db.session.commit()
        except Exception as e:
            print(e)
            return {"status": "failed"}
        try:
            data_object = Content(template_id=int(temp.template_id), ref_no=data_list[1], from_address=data_list[2],
                                  to_address=data_list[3], subject=data_list[4], body=data_list[5],
                                  sign_off=data_list[6], copy_to=data_list[7], date=date_object,
                                  occurence_date=data_list[9]['occurence_date'], venue=data_list[9]['venue'],
                                  starting_time=data_list[9]['starting_time'], ending_time=data_list[9]['ending_time'])
            db.session.add(data_object)
            db.session.commit()
            return {
                "status": "success",
                "id": temp.template_id
            }
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
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
            if data:
                return jsonify(data)
            else:
                return {"status": "no"}
        except Exception as e:
            print(e)
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
        except Exception as e:
            print(e)
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

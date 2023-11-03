from datetime import datetime

import sqlalchemy.exc
from flask import request, jsonify
from flask_restful import Resource
from model import *


class Generate(Resource):
    def post(self):
        data = request.form.to_dict() or request.json
        # data_list = list(data.values())
        print(data)
        # date_object = datetime.strptime(data_list[0], '%Y-%m-%d').date()
        temp = Template(template_name=data['template_name'])
        try:
            db.session.add(temp)
            db.session.commit()
        except Exception as e:
            print(e)
            return {"status": "failed"}
        try:
            data_object = Content(template_id=int(temp.template_id), from_address=data['from'],
                                  to_address=data['to'], subject=data['subject'], body=data['body'],
                                  sign_off=data['sign_off'], copy_to=data['copy_to'],
                                  occurence_date=data['selectedOptions']['occurence_date'],
                                  venue=data['selectedOptions']['venue'],
                                  starting_time=data['selectedOptions']['starting_time'],
                                  ending_time=data['selectedOptions']['ending_time'])
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
        data = Template.query.all()
        if data:
            return jsonify(data)
        else:
            return {"status": "no"}


class Circulars(Resource):
    def get(self):
        ref_no = request.args.get("id")
        if ref_no:
            data = Circular.query.filter_by(ref_no=ref_no).first()
            if data:
                return jsonify(data)
            else:
                return {"status": "no"}
        data = Announcement.query.all()
        if data:
            return jsonify(data)
        else:
            return {"status": "no"}

    def post(self):
        data = request.form.to_dict() or request.json
        # date_object = datetime.strptime(data['date'], '%Y-%m-%d').date()
        try:
            announcement = Announcement(ref_no=data['ref_no'], circular_name=data['circular_name'])
            db.session.add(announcement)
            data_object = Circular(ref_no=data['ref_no'], from_address=data['from_address'], to_address=data['to_address'],
                                   subject=data['subject'], body=data['body'], date=datetime.date.today(),
                                   sign_off=data['sign_off'], copy_to=data['copy_to'],
                                   occurence_date=data['occurence_date'], venue=data['venue'],
                                   starting_time=data['starting_time'], ending_time=data['ending_time'])
            db.session.add(data_object)
            db.session.commit()
            return {
                "status": "success",
                "circular_id": data['ref_no']
            }
        except Exception as e:
            print(e)
            return {"status": "Failure"}


class Login(Resource):
    def post(self):
        try:
            data = request.form.to_dict() or request.json
            query = Users.query.filter_by(staff_id=int(data["staff_id"]),password=data["password"]).first()
            if query:
                return {"status": "Success"}
            else:
                return {"status": "Invalid"}
        except Exception as e:
            return {"status": "Failure"}
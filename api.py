from datetime import datetime as dt
import json
import sqlalchemy.exc
from flask import request, jsonify
from flask_login import login_required
from flask_restful import Resource
from flask_security import auth_required, roles_accepted

from model import *


class Generate(Resource):
    # @auth_required("token")
    # @roles_accepted("admin")
    def post(self):
        data = request.form.to_dict() or request.json
        print(data)
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
                                  occurrence_date=data['selectedOptions']['occurrence_date'],
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

    # @auth_required("token")
    # @roles_accepted("admin")
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

    # @auth_required("token")
    # @roles_accepted("admin")
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
    # @auth_required("token")
    # @roles_accepted("admin")
    def get(self):
        data = Template.query.all()
        if data:
            return jsonify(data)
        else:
            return {"status": "no"}


class Circulars(Resource):
    # @auth_required("token")
    def get(self):
        ref_no = request.args.get("id")
        if ref_no:
            data = Circular.query.filter_by(ref_no=ref_no).first()
            circular_dict = data.to_dict()
            if data:
                return jsonify(circular_dict)
            else:
                return {"status": "no"}
        data = Announcement.query.all()
        if data:
            return jsonify(data)
        else:
            return {"status": "no"}
        
        
    # @auth_required("token")
    # @roles_accepted("admin")
    def post(self):
        data = request.form.to_dict() or request.json
        date_format = "%Y-%m-%d"
        time_format = "%H:%M"
        print(data)
        try:
            announcement = Announcement(ref_no=data['ref_no'], circular_name=data['circular_name'])
            db.session.add(announcement)
            data_object = Circular(ref_no=data['ref_no'], from_address=data['from_address'], to_address=data['to_address'],
                               subject=data['subject'], body=data['body'],
                               date=dt.strptime(data['date'], date_format),
                               sign_off=data['sign_off'], copy_to=data['copy_to'],
                               occurrence_date=dt.strptime(data['occurrence_date'], date_format).date() if data['occurrence_date'] else None,
                               venue=data['venue'],
                               starting_time=dt.strptime(data['starting_time'], time_format).time() if data['starting_time'] else None,
                               ending_time=dt.strptime(data['ending_time'], time_format).time() if data['ending_time'] else None)
            db.session.add(data_object)
            db.session.commit()
            return {
                "status": "success",
                "circular_id": data['ref_no']
            }
        except Exception as e:
            print(e)
            return {"status": "Failure"}
        
    # @auth_required("token")
    # @roles_accepted("admin")    
    def delete(self):
        try:
            ref_no = request.args.get('ref_no')
            if ref_no:
                data = Circular.query.filter_by(ref_no=ref_no).first()
                content = Announcement.query.filter_by(ref_no=ref_no).first()
                db.session.delete(data)
                db.session.commit()
                db.session.delete(content)
                db.session.commit()
                return {"status": "success"}
        except Exception as e:
            print(e)
            return {"status": "failed"}


class Login(Resource):
    def post(self):
        try:
            data = request.form.to_dict() or request.json
            query = User.query.filter_by(staff_id=int(data["staff_id"]),password=data["password"]).first()
            if query:
                return {"status": "Success"}
            else:
                return {"status": "Invalid"}
        except Exception as e:
            return {"status": "Failure"}
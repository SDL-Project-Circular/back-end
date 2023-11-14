import datetime
from flask_security import UserMixin, RoleMixin
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, Date, DateTime, Time
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from datetime import date
from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()


@dataclass
class Content(db.Model):
    template_id: int = Column(Integer, ForeignKey("template.template_id"), nullable=False)
    content_id: int = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    from_address: str = Column(String, nullable=False)
    to_address: str = Column(String, nullable=False)
    subject: str = Column(String, nullable=False)
    body: str = Column(String, nullable=False)
    sign_off: str = Column(String, nullable=False)
    copy_to: str = Column(String, nullable=False)
    occurrence_date: bool = Column(Boolean, nullable=True, default=False, unique=False)
    venue: bool = Column(Boolean, nullable=True, default=False, unique=False)
    starting_time: bool = Column(Boolean, nullable=True, default=False, unique=False)
    ending_time: bool = Column(Boolean, nullable=True, default=False, unique=False)


@dataclass
class Template(db.Model):
    template_id: int = Column(Integer, primary_key=True, autoincrement=True)
    template_name: str = Column(String, nullable=False)
    date: date = Column(Date, default=datetime.date.today())


@dataclass
class Circular(db.Model):
    circular_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    ref_no = Column(String, ForeignKey("announcement.ref_no"), nullable=False)
    from_address = Column(String, nullable=False)
    to_address = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(String, nullable=False)
    sign_off = Column(String, nullable=False)
    copy_to = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    occurrence_date = Column(Date, nullable=True, default=None, unique=False)
    venue = Column(String, nullable=True, default=None, unique=False)
    starting_time = Column(Time, nullable=True, default=None, unique=False)
    ending_time = Column(Time, nullable=True, default=None, unique=False)

    def to_dict(self):
        return {
            "circular_id": self.circular_id,
            "ref_no": self.ref_no,
            "from_address": self.from_address,
            "to_address": self.to_address,
            "subject": self.subject,
            "body": self.body,
            "sign_off": self.sign_off,
            "copy_to": self.copy_to,
            "date": self.date.isoformat(),
            "occurrence_date": self.occurrence_date.isoformat() if self.occurrence_date else None,
            "venue": self.venue,
            "starting_time": self.starting_time.strftime("%H:%M") if self.starting_time else None,
            "ending_time": self.ending_time.strftime("%H:%M") if self.ending_time else None
        }


@dataclass
class Announcement(db.Model):
    ref_no: str = Column(String, primary_key=True, nullable=False)
    circular_name: str = Column(String, nullable=False, unique=True)
    date: date = Column(Date, default=datetime.date.today())


#
# @dataclass
# class Users(db.Model, UserMixin):
#     staff_id: int = Column(Integer, primary_key=True, nullable=False)
#     password: str = Column(String, nullable=False)
#     active: bool = Column(Boolean)
#     fs_uniquifier: str = Column(String, unique=True, nullable=False)
#     roles = db.relationship('Role', secondary="rolesusers", backref=db.backref("Users", lazy="dynamic"))
#
#
# @dataclass
# class Role(db.Model, RoleMixin):
#     id: int = Column(Integer, primary_key=True)
#     name: str = Column(String, nullable=False, unique=True)
#     description: str = Column(String)
#
#
# @dataclass
# class RolesUsers(db.Model):
#     id: int = Column(Integer, primary_key=True)
#     user_id: int = Column(Integer, ForeignKey('users', 'staff_id'))
#     role_id: int = Column(Integer, ForeignKey('role', 'id'))


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=False)
    email = db.Column(db.String(255), unique=True, index=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='roles_users',
                            backref=db.backref('users', lazy='dynamic'))
    # study_resource = db.relationship('StudyResource', backref='creator')


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

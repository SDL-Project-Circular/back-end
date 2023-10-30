from sqlalchemy import Column, Boolean , Integer, String, ForeignKey, Date
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from datetime import date
from sqlalchemy.orm import relationship

db = SQLAlchemy()


@dataclass
class Content(db.Model):
    template_id: int = Column(Integer, ForeignKey("template.template_id"), nullable=False)
    ref_no: str = Column(String, nullable=False, primary_key=True)
    from_address: str = Column(String, nullable=False)
    to_address: str = Column(String, nullable=False)
    subject: str = Column(String, nullable=False)
    body: str = Column(String, nullable=False)
    sign_off: str = Column(String, nullable=False)
    copy_to: str = Column(String, nullable=False)
    date: date = Column(Date, nullable=False)
    occurence_date: bool = Column(Boolean, nullable=True, default=False, unique=False)
    venue: bool = Column(Boolean, nullable=True, default=False, unique=False)
    starting_time: bool = Column(Boolean, nullable=True, default=False, unique=False)
    ending_time: bool = Column(Boolean, nullable=True, default=False, unique=False)


@dataclass
class Template(db.Model):
    template_id: int = Column(Integer, primary_key=True, autoincrement=True)
    template_name: str = Column(String, nullable=False)

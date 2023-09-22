from .extensions import db 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base

class SMSMessage(Base):
    __tablename__ = 'sms_messages'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    result = db.Column(db.String(20))

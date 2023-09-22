from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from .app import main

db = create_engine('postgresql://sms_messages_user:leMmtPVKr4TFxdudP6hYBPWPSnKRtr7Q@dpg-ck624kgs0i2c73chms00-a.oregon-postgres.render.com/sms_messages')

Session = sessionmaker(bind=db)

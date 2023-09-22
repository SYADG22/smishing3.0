from flask_sqlalchemy import SQLAlchemy
from .app import main

db = SQLAlchemy(main)

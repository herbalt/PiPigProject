"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask('microblog')
app.config.from_object('config')
db = SQLAlchemy(app)
"""






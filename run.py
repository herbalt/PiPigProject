from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from microblog import app, db
from microblog.app_config import config_class

if __name__ == '__main__':
    app.debug = config_class.DEBUG
    db.create_all(app=app)
    app.run()




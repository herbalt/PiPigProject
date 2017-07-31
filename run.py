from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pipig import app, db
from pipig.app_config import config_class

from sensors.data_setup import data_setup as data_setup_sensors

if __name__ == '__main__':
    app.debug = config_class.DEBUG
    db.create_all(app=app)

    with app.app_context():
        data_setup_sensors()

    app.run()






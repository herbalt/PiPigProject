from flask import Flask, render_template

from pipig.auth import login_manager
import pipig.errors as errors
import pipig.logs as logs
from app_config import config_class as config
from mail import mail



# BLUEPRINTS
#from pipig.users.views import users
from database.views import database


from pipig.data import db

app = Flask(__name__)
app.config.from_object(config)

# Setup extensions
db.init_app(app)
login_manager.init_app(app)
mail.init_app(app)

# Internal extensions for managing
# logs and adding error handlers

# logs.init_app(app, remove_existing_handlers=True)
# errors.init_app(app)

# app.register_blueprint(users)
# app.register_blueprint(database)




from pipig.sensors.views import sensors
from pipig.sessions.views import sessions
from pipig.appliances.views import appliances
from pipig.recipes.views import recipes

from pipig.binders.views import binders
from pipig.data_points.views import data_points
from pipig.generics.views import generics
from pipig.gpio_pins.views import gpio_pins


app.register_blueprint(sensors)
app.register_blueprint(sessions)
app.register_blueprint(recipes)
app.register_blueprint(appliances)
app.register_blueprint(binders)
app.register_blueprint(data_points)
app.register_blueprint(generics)
app.register_blueprint(gpio_pins)

@app.route('/')
def index():
    return render_template('index.html', user=None)


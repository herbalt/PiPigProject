from flask import Flask, Blueprint

# import logs
from app_config import config_class as config
from mail import mail

from .api import api as api_plus
from .auth import login_manager

from .api.sensors.endpoints import sensor_namespace
from .api.appliances.endpoints import appliance_namespace
from .api.recipes.endpoints import recipe_namespace
from .api.datapoints.endpoints import datapoints_namespace
from .api.raspberry_pi.endpoints import pi_namespace
from .api.pi_pig.endpoints import pipig_namespace


app = Flask(__name__)
app.config.from_object(config)

blueprint = Blueprint('api', __name__, url_prefix='/api')
api_plus.init_app(blueprint)

api_plus.add_namespace(sensor_namespace)
api_plus.add_namespace(appliance_namespace)
api_plus.add_namespace(recipe_namespace)
api_plus.add_namespace(datapoints_namespace)
api_plus.add_namespace(pi_namespace)
api_plus.add_namespace(pipig_namespace)


app.register_blueprint(blueprint)


from pipig.data import db
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




from .sensors.views import sensors
from .curing_sessions.views import sessions
from .appliances.views import appliances
from .recipes.views import recipes

from .binders.views import binders
from .data_points.views import data_points
from .generics.views import generics
from .pi_gpio.views import gpio_pins
from .pi_pig.views import pipig_blueprint as pipig_blueprint



app.register_blueprint(sensors)
app.register_blueprint(sessions)
app.register_blueprint(recipes)
app.register_blueprint(appliances)
app.register_blueprint(binders)
app.register_blueprint(data_points)
app.register_blueprint(generics)
app.register_blueprint(gpio_pins)
app.register_blueprint(pipig_blueprint)


pipig_instance = None

"""
@app.route('/')
def index():
    return render_template('index.html', user=None)
"""


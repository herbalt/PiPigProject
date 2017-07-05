from flask import Flask, Blueprint

from api.sensors.endpoint import sensor_namespace
from api.appliances.endpoint import appliance_namespace
from app_config import config_class as config
from mail import mail
from pipig.api import api as api_plus
from pipig.auth import login_manager

app = Flask(__name__)
app.config.from_object(config)

blueprint = Blueprint('api', __name__, url_prefix='/api')
api_plus.init_app(blueprint)
api_plus.add_namespace(sensor_namespace)
api_plus.add_namespace(appliance_namespace)
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




from pipig.sensors.views import sensors
from pipig.curing_sessions.views import sessions
from pipig.appliances.views import appliances
from pipig.recipes.views import recipes

from pipig.binders.views import binders
from pipig.data_points.views import data_points
from pipig.generics.views import generics
from pipig.pi_gpio.views import gpio_pins


app.register_blueprint(sensors)
app.register_blueprint(sessions)
app.register_blueprint(recipes)
app.register_blueprint(appliances)
app.register_blueprint(binders)
app.register_blueprint(data_points)
app.register_blueprint(generics)
app.register_blueprint(gpio_pins)




"""
@app.route('/')
def index():
    return render_template('index.html', user=None)
"""


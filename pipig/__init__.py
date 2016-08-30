from flask import Flask, render_template
from .data import db
from .auth import login_manager
import pipig.errors as errors
import pipig.logs as logs
from app_config import config_class as config
from mail import mail

# BLUEPRINTS
from .users.views import users
from database.views import database


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

app.register_blueprint(users)
app.register_blueprint(database)

if __name__ == '__main__':
    pass


@app.route('/')
def index():
    return render_template('index.html', user=None)


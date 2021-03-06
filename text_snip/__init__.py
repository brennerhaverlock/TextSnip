from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from text_snip.config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

###########################
# Authentication
###########################

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from text_snip.models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

bcrypt = Bcrypt(app)


###########################
# Blueprints
###########################

from text_snip.main.routes import main, auth
app.register_blueprint(main)
app.register_blueprint(auth)

with app.app_context():
    db.create_all()

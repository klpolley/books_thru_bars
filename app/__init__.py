from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
login = LoginManager(app)
login.login_view = 'login'
login.init_app(app)
login.session_protection = "strong"
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)

mail = Mail(app)

from app import routes, errors, login



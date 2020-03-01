from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
login = LoginManager(app)
bcrypt = Bcrypt(app)


from app import routes

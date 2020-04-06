from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

app.secret_key = 'BTB key'

app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = 1
app.config["MAIL_USERNAME"] = 'booksthrubars@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'booksthrubars@gmail.com'
app.config["MAIL_PASSWORD"] = 'angler$$'

mail = Mail(app)


from app import routes, errors



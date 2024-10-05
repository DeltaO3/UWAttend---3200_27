from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_apscheduler import APScheduler
from flask_mail import Mail, Message
from sqlalchemy import MetaData
import os

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)


login = LoginManager(app)
login.login_view = '/login'

from app import routes, models, database

#schedule
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

scheduler.add_job(
    id='Scheduled Task',
    func=database.delete_expired_units,  
    trigger='interval',  
    hours=24  
)

mail = Mail(app)

app.config['MAIL_SERVER'] = 'email-smtp.southeast-1.amazonaws.com'  
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('SES_SMTP_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('SES_SMTP_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = ('UWAttend Team', 'noreply@uwaengineeringprojects.com')

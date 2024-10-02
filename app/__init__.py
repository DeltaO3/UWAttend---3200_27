from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_apscheduler import APScheduler
from sqlalchemy import MetaData

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

# configuration of mail 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'cist3200team27testing@gmail.com'
app.config['MAIL_PASSWORD'] = 'secure_testing_password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app) 

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

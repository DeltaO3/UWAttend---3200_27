from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_apscheduler import APScheduler

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
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

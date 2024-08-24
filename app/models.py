from flask_sqlalchemy import SQLAlchemy
from app import app
from app import db


# admin, this is the classes that are allocated to each staff member by the admin
# the values here will be listed in /Sessions/ so a faculty can only select what they are
# allocated

#class administrator(db.Model):
#   UnitName = 
#   UnitCode =
#   UserId   =
#   what else is needed we can talk about at meetings?



# attendance data, values that are set by slqite db are not defined here
class attendance_data(db.Model):
        
    AttendanceId = db.Column(db.Text, primary_key = True)
    UnitId = db.Column(db.Text)
    StudentId = db.Column(db.Text)
    Surname = db.Column(db.Text) 
    Title = db.Column(db.Text)
    PreferedName = db.Column(db.Text)
    DateTime = db.Column(db.Text)
    PeriodOfDay = db.Column(db.Text)
    Consent = db.Column(db.Text)
    AttendanceMarked = db.Column(db.Text)
    SessionId = db.Column(db.Integer)



# 
class session_data(db.Model):

    SessionId = db.Column(db.Text, primary_key=True)
    UserId = db.Column(db.Text)
    UnitName = db.Column(db.Text)
    UnitCode = db.Column(db.Text)


class login_data(db.Model):

    UserId = db.Column(db.Integer, primary_key = True)
    Username = db.Column(db.Text)
    Hash = db.Column(db.Text)
    


    

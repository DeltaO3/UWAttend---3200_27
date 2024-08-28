from flask_sqlalchemy import SQLAlchemy
from app import app
from app import db
from datetime import datetime

# admin, this is the classes that are allocated to each staff member by the admin
# the values here will be listed in /Sessions/ so a faculty can only select what they are
# allocated
#class administrator(db.Model):
#   UnitName = 
#   UnitCode =
#   UserId   =
#   what else is needed we can talk about at meetings?

# AttendanceId should be populated with data from a google sheets file with the students information, until we get that file the studentId will be populated with the students name
class attendance_data(db.Model):
        
    AttendanceId = db.Column(db.Text, primary_key = True)    # will be populated with data from the google sheets callista, atm its just the students name for testing purposes
    UnitId = db.Column(db.Text) 
    StudentId = db.Column(db.Text)     # callista provides this or user input
    Surname = db.Column(db.Text)       # callista provides this
    Title = db.Column(db.Text)         # callista provides this
    PreferredName = db.Column(db.Text)  # callista provides this
    DateTime = db.Column(db.Text, default=datetime.now().strftime("%Y%m%d%H%M"))
    SignedOut = db.Column(db.Text)                           # empty until the sign all out button is pressed
    PeriodOfDay = db.Column(db.Text)
    Consent = db.Column(db.Text, default="no")
    AttendanceMarked = db.Column(db.Text, default="yes")     # defaults because its assumed when this function is used the attendance is getting marked
    SessionId = db.Column(db.Integer)                        # this is a foreign key defined in the database itself

# The Primary Key is a combination of (DateTime() + UnitCode)
# UserId : this is who is running the class and configured the session
class session_data(db.Model):

    SessionId = db.Column(db.Text, primary_key=True)
    UserId = db.Column(db.Text)                # this is a foreign key defined in the database itself
    UnitName = db.Column(db.Text)
    UnitCode = db.Column(db.Text)
    DateTime = db.Column(db.Text, default=datetime.now().strftime("%Y%m%d%H%M"))  # defaults to when session is created

# renamed to login_data to avoid issues with other imported modules 
class login_data(db.Model):

    UserId = db.Column(db.Integer, primary_key = True)
    Username = db.Column(db.Text)
    Hash = db.Column(db.Text)
    


    

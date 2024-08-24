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

# AttendanceId will be populated with data from a google sheets file with the students information, until we get that file the studentId will be populated with the students name
# the below values are automatically assigned their values by the database but we could change this, they wont need user input at the moment
# DateTime          # defaults to CURRENT_TIMESTAMP
# SignedOut         # defaults to CURRENT_TIMESTAMP
# attendanceMarked  # defaults to "yes"
class attendance_data(db.Model):
        
    AttendanceId = db.Column(db.Text, primary_key = True)
    UnitId = db.Column(db.Text)
    StudentId = db.Column(db.Text)
    Surname = db.Column(db.Text) 
    Title = db.Column(db.Text)
    PreferedName = db.Column(db.Text)
    DateTime = db.Column(db.Text)
    SignedOut = db.Column(db.Text)
    PeriodOfDay = db.Column(db.Text)
    Consent = db.Column(db.Text)
    AttendanceMarked = db.Column(db.Text)
    SessionId = db.Column(db.Integer)        # this is a foreign key defined in the database itself

# The Primary Key is a combination of (DateTime() + UnitCode)
# UserId : this is who is running the class and configured the session
class session_data(db.Model):

    SessionId = db.Column(db.Text, primary_key=True)
    UserId = db.Column(db.Text)                # this is a foreign key defined in the database itself
    UnitName = db.Column(db.Text)
    UnitCode = db.Column(db.Text)

# renamed to login_data to avoid issues with other imported modules 
class login_data(db.Model):

    UserId = db.Column(db.Integer, primary_key = True)
    Username = db.Column(db.Text)
    Hash = db.Column(db.Text)
    


    

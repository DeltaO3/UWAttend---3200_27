import flask
from app import app
from app import db
from .models import db, Student, User, Attendance, Session, Unit
from datetime import datetime
from app.helpers import get_perth_time

# sql
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

def SignOut(studentID, sessionID):
    
    ## IMPORTANT
    # this may have a glitch where there are multiple rows with the same sessionID
    # and studentID which will confuse the query, for now im hoping the first() will naturally pick the most recent sessionID row with a blank signoutTime column instead of a row from weeks ago
    
    new_signOutTime = get_perth_time().time()
    
    query = db.session.query(Attendance)
    attendance_record = query.filter( and_(Attendance.studentID == studentID,Attendance.sessionID == sessionID, Attendance.signOutTime == None )).first()
   
    
    # If the record exists, update the signOutTime
    if attendance_record:
        attendance_record.signOutTime = new_signOutTime
        db.session.commit()
        print(f"SignOutTime updated ")
    else:
        print(f"No attendance record found ")

# Helper to check for duplicate students
def student_exists(student_number):
    return db.session.query(Student).filter_by(studentNumber=student_number).first() is not None

def AddStudent(studentID, studentNumber, firstName, lastName, title, preferredName, unitID, consent):    
   
    try:
        StudentEntry = Student(
            studentID       = studentID,
            studentNumber   = studentNumber,
            firstName       = firstName,
            lastName        = lastName,
            title           = title,
            preferredName   = preferredName,
            unitID          = unitID,
            consent         = consent)            

        db.session.add(StudentEntry)    # add the changes 
        db.session.commit()             # save the changes
    
    except IntegrityError as e:
        db.session.rollback()
        print(f'An error occurred: {e}')  

   

def AddSession(sessionID, unitID, sessionName, sessionTime, sessionDate):
    
    try:
        SessionEntry = Session(
            sessionID   = sessionID,
            unitID      = unitID,
            sessionName = sessionName,
            sessionTime = sessionTime,
            sessionDate = sessionDate)

        db.session.add(SessionEntry)    # add the changes 
        db.session.commit()             # save the changes
    
    except IntegrityError as e:
        db.session.rollback()
        print(f'An error occurred: {e}')

   

def AddAttendance(attendanceID, sessionID, studentID, signOutTime=None, facilitatorID=None, marks=None, comments=None, consent_given=None):

    new_signInTime = get_perth_time().time()
    
    try:
        AttendanceEntry = Attendance(
            attendanceID    = attendanceID,
            sessionID       = sessionID,
            studentID       = studentID,
            signInTime      = new_signInTime,
            signOutTime     = signOutTime,
            facilitatorID   = facilitatorID,
            marks           = marks,
            comments        = comments,
            consent_given   = consent_given)
               

        db.session.add(AttendanceEntry)    # add the changes 
        db.session.commit()             # save the changes
    
    except IntegrityError as e:
        db.session.rollback()
        print(f'An error occurred: {e}')

    

def AddUser(uwaID, firstName, lastName, passwordHash, userType):

    try:
        UserEntry = User(
            uwaID       = uwaID,
            firstName   = firstName,
            lastName    = lastName,
            passwordHash = passwordHash,
            userType    = userType)

        db.session.add(UserEntry)    # add the changes 
        db.session.commit()             # save the changes
    
    except IntegrityError as e:
        db.session.rollback()
        print(f'An error occurred: {e}')

    

def AddUnit(unitID, unitCode, unitName, studyPeriod, active, startDate, endDate, sessionNames, sessionTimes, comments, marks, consent, commentSuggestions):

    try:
        UnitEntry   = Unit(
            unitID       = unitID,
            unitCode     = unitCode,
            unitName     = unitName,
            studyPeriod  = studyPeriod,
            active       = active,
            startDate    = startDate,
            endDate      = endDate,
            sessionNames = sessionNames,
            sessionTimes = sessionTimes,
            comments     = comments,
            marks        = marks,
            consent      = consent,
            commentSuggestions = commentSuggestions)            
               

        db.session.add(UnitEntry)       # add the changes 
        db.session.commit()             # save the changes
    
    except IntegrityError as e:
        db.session.rollback()
        print(f'An error occurred: {e}')

   

def GetAttendance(attendanceID = None, input_sessionID = None, studentID = None):

    query = db.session.query(Attendance)
    
    # handle the optional arguements, only one can be used 
    if attendanceID is not None:
        query = query.filter(Attendance.attendanceID == attendanceID)
    elif input_sessionID is not None:
        query = query.filter(Attendance.sessionID == input_sessionID)
    elif studentID is not None:
        query = query.filter(Attendance.studentID == studentID)
    else:
        # no parameters were supplied.
        print("You did not submit a parameter to use so returning all attendence records")

    
    attendance_records = query.all()
    
    
    return attendance_records

def GetSession(sessionID = None, unitID = None):

    query = db.session.query(Session)
    
    # handle the optional arguements, only one can be used 
    if sessionID is not None:
        query = query.filter(Session.sessionID == sessionID)
    elif unitID is not None:
        query = query.filter(Session.unitID == unitID)
    else:
        # no parameters were supplied.
        print("You did not submit a parameter to use so returning all session records")

    
    attendance_records = query.all()
    
    return attendance_records

def GetStudent(unitID = None, studentID = None, studentNumber = None):

    query = db.session.query(Student)
    
    # handle the optional arguements, only one can be used 
    if unitID is not None:
        query = query.filter(Student.unitID == unitID)
    elif studentID is not None:
        query = query.filter(Student.studentID == studentID)
    elif studentNumber is not None:
        query = query.filter(Student.studentNumber == studentNumber)
    else:
        # no parameters were supplied.
        print("You did not submit a parameter to use so returning all student records")

    
    attendance_records = query.all()
    
    return attendance_records

def GetUser(userID = None, uwaID = None, userType = None):

    query = db.session.query(User)
    
    # handle the optional arguements, only one can be used 
    if userID is not None:
        query = query.filter(User.userID == userID)
    elif uwaID is not None:
        query = query.filter(User.uwaID == uwaID)
    elif userType is not None:
        query = query.filter(User.userType == userType)
    else:
        # no parameters were supplied.
        print("You did not submit a parameter to use so returning all user records")

    
    attendance_records = query.all()
    
    return attendance_records

def GetUnit(unitID = None, unitCode = None, studyPeriod = None):

    query = db.session.query(Unit)

    # handle the optional arguements, only one can be used
    if unitID is not None:
        query = query.filter(Unit.unitID == unitID)
    elif unitCode is not None:
        query = query.filter(Unit.unitCode == unitCode)
    elif studyPeriod is not None:
        query = query.filter(Unit.studyPeriod == studyPeriod)
    else:
        # no parameters were supplied.
        print("You did not submit a parameter to use so returning all unit records")


    unit_records = query.all()

    return unit_records

import flask
from app import app
from app import db
from .models import db, Student, User, Attendance, Session, Unit
from datetime import datetime, date, timedelta
from app.helpers import get_perth_time

# sql
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, func
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
def student_exists(student_number, unit_code):
    return db.session.query(Student).filter_by(studentNumber=student_number, unitID=unit_code).first() is not None

def unit_exists(unit_code, start_date):
    return db.session.query(Unit).filter_by(unitCode=unit_code, startDate=start_date).first() is not None

def AddStudent(studentNumber, firstName, lastName, title, preferredName, unitID, consent):    
   
    try:
        StudentEntry = Student(
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

   
# returns the session that was just created
def AddSession(unitID, sessionName, sessionTime, sessionDate):
    
    try:
        SessionEntry = Session(
            unitID      = unitID,
            sessionName = sessionName,
            sessionTime = sessionTime,
            sessionDate = sessionDate)

        db.session.add(SessionEntry)    # add the changes 
        db.session.commit()             # save the changes
    
    except IntegrityError as e:
        db.session.rollback()
        print(f'An error occurred: {e}')

    return GetUniqueSession(unitID, sessionName, sessionTime, sessionDate)

   

def AddAttendance(sessionID, studentID, signOutTime=None, facilitatorID=None, marks=None, comments=None, consent_given=None):

    new_signInTime = get_perth_time().time()
    
    try:
        AttendanceEntry = Attendance(
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

    

def AddUser(email, firstName, lastName, passwordHash, userType):

    try:
        UserEntry = User(
            email       = email,
            firstName   = firstName,
            lastName    = lastName,
            passwordHash = "",
            userType    = userType)

        UserEntry.set_password(passwordHash)
        
        db.session.add(UserEntry)    # add the changes 
        db.session.commit()             # save the changes
    
    except IntegrityError as e:
        db.session.rollback()
        print(f'An error occurred: {e}')

def UpdateUser(email, firstName, lastName, passwordHash): # no userType as this should already be set 

    user = GetUser(email)
    
    if not user:
        print("User not found")
        return

    try:
        user.firstName = firstName
        user.lastName = lastName
        user.set_password(passwordHash)  

        db.session.commit()
        print("User details updated")
    
    except IntegrityError as e:
        db.session.rollback()
        print(f'An error occurred: {e}')


def AddUnit(unitCode, unitName, studyPeriod, startDate, endDate, sessionNames, sessionTimes, comments, marks, consent, commentSuggestions):

    try:
        UnitEntry   = Unit(
            unitCode     = unitCode,
            unitName     = unitName,
            studyPeriod  = studyPeriod,
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

        return db.session.query(Unit).filter_by(unitCode=unitCode, startDate=startDate).first().unitID
    
    except IntegrityError as e:
        db.session.rollback()
        print(f'An error occurred: {e}')

def AddUnitToCoordinator(email, unitID):
    user = db.session.query(User).filter_by(email=email).first()
    unit = db.session.query(Unit).filter_by(unitID=unitID).first()
    user.unitsCoordinate.append(unit)
    unit.coordinators.append(user)
    db.session.commit()

def AddUnitToFacilitator(email, unitID):
    user = db.session.query(User).filter_by(email=email).first()
    unit = db.session.query(Unit).filter_by(unitID=unitID).first()
    user.unitsFacilitate.append(unit)
    unit.facilitators.append(user)
    db.session.commit()


#Do get functions need primary key IDs?

def GetAttendanceByIDAndFacilitator(sessionID, facilitatorID):
    query = db.session.query(Attendance).filter(Attendance.sessionID == sessionID, Attendance.facilitatorID == facilitatorID)
    attendance_records = query.all()
    return attendance_records

def GetAttendance(attendanceID = None, input_sessionID = None, studentID = None):

    query = db.session.query(Attendance)
    
    # handle the optional arguements, only one can be used 
    if studentID is not None and input_sessionID is not None:
        query = query.filter(Attendance.studentID == studentID, Attendance.sessionID == input_sessionID)
    elif attendanceID is not None:
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

# queries db for a specific (unique) session, all inputs required
# returns the session (or none if session doesn't exist)
def GetUniqueSession(unitID, sessionName, sessionTime, sessionDate):

    session = db.session.query(Session).filter(Session.unitID == unitID,
                                             Session.sessionName == sessionName,
                                             Session.sessionTime == sessionTime,
                                             Session.sessionDate == sessionDate
                                             ).first()
    return session

def GetSession(sessionID = None, unitID = None, return_all = False):

    query = db.session.query(Session)
    
    # handle the optional arguements, only one can be used 
    if sessionID is not None:
        query = query.filter(Session.sessionID == sessionID)
    elif unitID is not None:
        query = query.filter(Session.unitID == unitID)
    elif not return_all:
        return
        # no parameters were supplied.
        # print("You did not submit a parameter to use so returning all session records")

    
    attendance_records = query.all()
    
    return attendance_records

# Specifically for exporting to csv ONLY. GetSession() was changed so creating seperate function so sessions dont break
def GetSessionForExport(sessionID = None, unitID = None):

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
    if studentID is not None and unitID is not None:
        query = query.filter(Student.unitID == unitID, Student.studentID == studentID)
    elif unitID is not None:
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

def GetStudentList(student_ids):

    query = db.session.query(Student)
    
    # handle the optional arguements, only one can be used 
    if student_ids is not None:
        query = query.filter(Student.studentID.in_(student_ids))
    else:
        # no parameters were supplied.
        print("You did not submit a parameter to use so returning all student records")

    
    attendance_records = query.all()
    
    return attendance_records

def GetUser(userID = None, email = None, userType = None):

    query = db.session.query(User)
    
    # handle the optional arguements, only one can be used 
    if userID is not None:
        query = query.filter(User.userID == userID)
    elif email is not None:
        query = query.filter(User.email == email)
    elif userType is not None:
        query = query.filter(User.userType == userType)
    else:
        # no parameters were supplied.
        print("You did not submit a parameter to use so returning all user records")

    
    attendance_records = query.first()
    
    return attendance_records

# Used for exporting to csv. Required because can't change GetUser() to return query.all() instead of query.first()
def GetAllUsers():
    query = db.session.query(User)

    return query.all()

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

#Is this function needed? dont see it used anywhere
def SetPassword(email, newPassword):
    
    user = db.session.query(User).filter(User.email == email).first()
    
    if user is None:
        raise ValueError("User not found")    

    # Set the new password hash
    user.set_password(newPassword)
    
    # Commit the changes to the database
    db.session.commit()


def RemoveStudentFromSession(studentID, sessionID):
    attendance_record = db.session.query(Attendance).filter_by(studentID=studentID, sessionID=sessionID).first()

    if attendance_record:
        db.session.delete(attendance_record)
        db.session.commit()
        return True

    else:
        return False
    
def EditAttendance(sessionID, studentID, signInTime=None, signOutTime=None, login=None, consent=None, grade=None, comments=None):
    # Fetch the attendance record based on studentID
    attendance_record = db.session.query(Attendance).filter_by(studentID=studentID, sessionID=sessionID).first()
    unitID = GetSession(sessionID=sessionID)[0].unitID
    consent_required_for_unit = GetUnit(unitID=unitID)[0].consent
    student_record = db.session.query(Student).filter_by(studentID=studentID, unitID=unitID).first()

    if not attendance_record:
        message = f"Attendance record for student ID {studentID} not found."
        return message
    
    if signOutTime and signInTime:
        if signOutTime < signInTime:
            message = "Sign out time cannot be before sign in time."
            return message

    # Update only the fields that are passed
    if signInTime:
        try:
            # Convert signInTime string to a Python time object
            attendance_record.signInTime = datetime.strptime(signInTime, '%H:%M:%S').time()
        except ValueError:
            message = f"Invalid time format for signInTime: {signInTime}"
            return message

    if signOutTime:
        try:
            # Convert signOutTime string to a Python time object
            attendance_record.signOutTime = datetime.strptime(signOutTime, '%H:%M:%S').time()
        except ValueError:
            message = f"Invalid time format for signOutTime: {signOutTime}"
            return message

    if login is not None:  # Boolean field
        if not login and not attendance_record.signOutTime:
            attendance_record.signOutTime = get_perth_time().time()
        if login and attendance_record.signOutTime:
            message = f"Student temporarily signed out between {str(attendance_record.signOutTime).split('.')[0]} and {str(get_perth_time().time()).split('.')[0]}"
            if comments: 
                comments = comments + f" | {message}"
            else:
                comments = message
            attendance_record.signOutTime = None

    if consent is not None:  # Boolean field
        student_record.consent = "yes" if consent else "no"
        attendance_record.consent_given = "yes" if consent else "no"

    if not consent_required_for_unit :
        student_record.consent = "not required"
        attendance_record.consent_given = "not required"

    if grade:
        attendance_record.marks = grade

    attendance_record.comments = comments

    # Commit the changes to the database
    try:
        db.session.commit()
        print(f"Attendance record for student ID {studentID} updated successfully.")
        return "True"
    except Exception as e:
        db.session.rollback()
        message = f"Error updating attendance record for student ID {studentID}: {e}"
        return message

def SignStudentOut(attendanceID):

    attendance = db.session.query(Attendance).filter(Attendance.attendanceID == attendanceID).first()

    if attendance is None:
        return False

    attendance.signOutTime = get_perth_time().time()

    db.session.commit()

    return True

def RemoveSignOutTime(attendanceID):

    attendance = db.session.query(Attendance).filter(Attendance.attendanceID == attendanceID).first()

    if attendance is None:
        return False

    comments = attendance.comments

    message = f"Student temporarily signed out between {str(attendance.signOutTime).split('.')[0]} and {str(get_perth_time().time()).split('.')[0]}"
    if comments: 
        comments = comments + f" | {message}"
    else:
        comments = message
    attendance.signOutTime = None
    attendance.comments = comments

    db.session.commit()

    return True

def delete_expired_units():
    # Wrap the function in the app context
    with app.app_context():
        try:
            # The query will work now as it has a proper Flask context
            today = date.today()
            year_ago = today - timedelta(days=365)
            expired_units = Unit.query.filter(Unit.endDate < year_ago).all()
            
            # Perform your deletion logic
            for unit in expired_units:
                # Delete the unit and associated records
                perform_delete_unit(unit.unitID)
                print(f"Deleted Unit ID: {unit.unitID}")
            
            db.session.commit()
            print("Successfully deleted expired units")
        except Exception as e:
            print(f"Error deleting units: {e}")
            db.session.rollback()

      
def perform_delete_unit(unit_id):
    try:
        # Step 1: Delete associated records from the Attendance table based on SessionID
        session_records = Session.query.filter_by(unitID=unit_id).all()
        for session in session_records:
            attendance_records = Attendance.query.filter_by(sessionID=session.sessionID).all()
            for attendance in attendance_records:
                db.session.delete(attendance)
                print(f"Deleting Attendance record for SessionID {session.sessionID}")

        # Step 2: Delete associated students from the Student table
        students = Student.query.filter_by(unitID=unit_id).all()
        for student in students:
            db.session.delete(student)  # Delete each student associated with the unit
            print(f"Deleting Student {student.studentID}")

        # Step 3: Delete associated records from the Sessions table
        session_records = Session.query.filter_by(unitID=unit_id).all()
        for session in session_records:
            db.session.delete(session)
            print(f"Deleting Session record for Unit {unit_id}")

        # Step 4: Delete the unit record from the Units table
        unit_record = Unit.query.filter_by(unitID=unit_id).first()
        if unit_record:
            db.session.delete(unit_record)
            print(f"Deleting Unit record for Unit {unit_id}")

        # Step 5: Commit all changes to the database
        db.session.commit()
        print(f"Successfully deleted Unit {unit_id} and all related records.")
    except Exception as e:
        # Rollback changes in case of an error
        print(f"Error deleting unit {unit_id}: {e}")
        db.session.rollback()


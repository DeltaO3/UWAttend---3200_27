import flask
from flask import send_file, redirect, url_for, after_this_request
from flask_login import current_user, login_user, logout_user, login_required
import os
from datetime import datetime
import sqlalchemy as sa

from app import app
from .forms import *
from .helpers import *
from .models import *
from .database import *
from .utilities import *
from app import database

# HOME -   /home/
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
@login_required
def home():
    form = StudentSignInForm()

    # TODO will need to be replaced with actual session logic later 
    current_session = GetSession(sessionID=1)[0]

    # get students who have signed in for this session
    attendance_records = GetAttendance(input_sessionID=current_session.sessionID)

    # get student IDs from the attendance records
    logged_in_student_ids = [str(record.studentID) for record in attendance_records]

    # get only the students who have logged in
    students = db.session.query(Student).filter(Student.studentID.in_(logged_in_student_ids)).all() # TODO should there be a database function for this?

    student_list = []
    signed_in_count = 0

    for student in students:
        # find the student's attendance record 
        attendance_record = next((record for record in attendance_records if record.studentID == student.studentID), None)

        # set login status based on whether the student has a time marked where they logged out
        login_status = "no" if attendance_record.signOutTime else "yes"

        signed_in_count = signed_in_count + 1 if login_status == "yes" else signed_in_count

        student_info = {
            "name": f"{student.preferredName} {student.lastName}",
            "number": student.studentNumber,
            "id": student.studentID,
            "login": login_status,  
            "photo": "yes" if student.consent == 1 else "no",
            "time": attendance_record.signInTime
        }
        student_list.append(student_info)

    student_list.sort(key=lambda x: x['time'], reverse=True)

    return flask.render_template('home.html', form=form, students=student_list, session=current_session, total_students=len(student_list), signed_in=signed_in_count, session_num=current_session.sessionID) 
	
# CONFIGURATION - /session/ /admin/
@app.route('/session', methods=['GET', 'POST'])
@login_required
def session():    
    form = SessionForm()
    # Get perth time
    perth_time = get_perth_time()
    humanreadable_perth_time = perth_time.strftime('%B %d, %Y, %H:%M:%S %Z')

    # For JS formatting
    formatted_perth_time = perth_time.isoformat()

    if form.validate_on_submit():
        # Handle form submission
        session_name = form.session_name.data
        unit_code = form.unit_code.data
        current_year = perth_time.year

        # Determine the semester based on the current month
        current_month = perth_time.month
        semester = "SEM1" if current_month <= 6 else "SEM2"
        # Create Database
        database_name = f"{unit_code}_{semester}_{current_year}"

        # Printing for debugging
        print(f"Session Name: {session_name}")
        print(f"Unit Code: {unit_code}")
        print(f"Semester: {semester}")
        print(f"Database Name: {database_name}")
        print(f"Current Date/Time: {humanreadable_perth_time}")
        # Redirect back to home page when done
	    
        return flask.redirect(flask.url_for('home'))

    return flask.render_template('session.html', form=form, perth_time=formatted_perth_time)

#ADMIM - /admin/
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.userType != 1:
        return flask.redirect('home')
    # I (James) do not know what to add here so for now it is blank


    return flask.render_template('admin.html')

# ADDUNIT - /addunit/ /admin/
@app.route('/addunit', methods=['GET', 'POST'])
@login_required
def addunit():
    if current_user.userType != 1:
        return flask.redirect('home')
    form = AddUnitForm()

    if form.validate_on_submit() and flask.request.method == 'POST':
        #Form data held here
        newunit_code = form.unitcode.data
        semester = form.semester.data
        consent_required = form.consentcheck.data
        start_date = form.startdate.data
        end_date = form.enddate.data
        student_file = form.studentfile.data
        facilitator_list = form.facilitatorlist.data
        sessionnames = form.sessionnames.data
        sessionoccurence = form.sessionoccurence.data
        assessmentcheck = form.assessmentcheck.data
        commentsenabled = form.commentsenabled.data
        commentsuggestions = form.commentsuggestions.data

        #Ensure is a new unit being added, QUESTION - is start date to be used?
        if unit_exists(newunit_code, start_date):
            error = "Unit and start date combo already exist in db"
            return flask.render_template('addunit.html', form=form, error=error)
        
        #Ensure end date is after start date
        if start_date > end_date:
            error = "Start date must be after end date"
            return flask.render_template('addunit.html', form=form, error=error)
        

        #convert session occurences to a | string
        occurences = ""
        for time in sessionoccurence:
            occurences += time + "|"
        occurences = occurences[:-1]
        print(f"session occurence string: {occurences}")

        #add to database
        unitID = AddUnit(newunit_code, "placeholdername", semester, 1, start_date, end_date, 
                sessionnames, occurences, commentsenabled , assessmentcheck, consent_required, commentsuggestions )
        
         #read CSV file
        if student_file.filename != '':
            student_file.save(student_file.filename)
            filename = student_file.filename
            process_csv(filename, unitID)
        else:
            print("Submitted no file, probable error.")
        
        #Handle facilitators
        #TODO: handle emailing facilitators, handle differentiating between facilitator and coordinator
        facilitators = facilitator_list.split('|')
        for facilitator in facilitators:
            if(not GetUser(uwaID=facilitator)):
                print(f"Adding new user: {facilitator}")
                AddUser(facilitator, "placeholder", "placeholder", facilitator, 3) #Do we assign coordinators?
            #add this unit to facilator
            print(f"Adding unit {unitID} to facilitator {facilitator}")
            AddUnitToFacilitator(facilitator, unitID)
        AddUnitToCoordinator(current_user.uwaID, unitID)
        
        return flask.redirect(flask.url_for('admin'))
	    
    return flask.render_template('addunit.html', form=form)

@app.route('/export', methods=['GET'])
@login_required
def export_data():
    print("Attempting to Export Database...")
    zip_filename = 'database.zip'

    # Get database.zip filepath
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    zip_path = os.path.join(project_root, zip_filename)

    # Call the function to export all data to the 'database.zip'
    export_all_to_zip(zip_filename)

    # Check if the file was created successfully
    if os.path.exists(zip_path):
        @after_this_request
        def delete_database(response):
            try:
                os.remove(zip_path)
                print("Temporary Database Deleted")
            except Exception as e:
                print(f"Error removing Temporary Database: {e}")
            return response

        # Serve the zip file for download
        response = send_file(zip_path, as_attachment=True)
        print("Admin Successfully Exported Database")
        return response

    else:
        # Handle the error if the zip file doesn't exist
        return "Error: Could not export the data.", 500


# STUDENT - /student/
@app.route('/student', methods=['POST'])
def student():
    student_id = flask.request.form['student_id']

    student = GetStudent(studentID=student_id)[0]

    # TODO will need to be replaced with actual session logic later
    current_session = GetSession(sessionID=1)[0]

    attendance_record = GetAttendance(input_sessionID=current_session.sessionID, studentID=student_id)[0] 

    login_status = "no" if attendance_record.signOutTime else "yes"

    if not student:
        flask.flash("Error - Student not found")
        return flask.redirect(flask.url_for('home'))
    
    student_info = {
        "name": f"{student.preferredName} {student.lastName}",
        "number": student.studentNumber,
        "id": student.studentID,
        "login": login_status,  
        "photo": "yes" if student.consent == 1 else "no",
        "time": attendance_record.signInTime
    }

    return flask.render_template('student.html', student=student_info)
	
# LOGIN - /login/ 
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        print("authenitcated")
        return flask.redirect('home')
    
    form = LoginForm()
    if form.validate_on_submit():
        user = database.GetUser(uwaID = form.username.data)                

        if user is None or not database.CheckPassword(form.username.data, form.password.data):
            flask.flash('Invalid username or password')
            return flask.redirect('login')
        
        login_user(user, remember=form.remember_me.data)
        return flask.redirect('home')

    return flask.render_template('login.html', form=form)

@app.route('/save_changes', methods=['POST'])
def save_changes():
    # Access form data 
    grade = flask.request.form.get('grade')
    comment = flask.request.form.get('comment')
    photo = flask.request.form.get('photo')

    # Process form data here (save changes to db)

    return flask.redirect('home') 

@app.route('/add_student', methods=['POST'])
def add_student():
    form = StudentSignInForm() # TODO still need a front-end prevention method for false sign ins 

    if form.validate_on_submit():
        # Handle form submission
        studentID = form.studentID.data
        consent_status = form.consent_status.data
        sessionID = form.sessionID.data

        print("Consent Status: ", consent_status)
        print("Session ID: ", sessionID)
        print("Student ID: ", studentID)

        session = GetSession(sessionID=sessionID)[0]
        unitID = session.unitID
        
        student = GetStudent(studentID=studentID, unitID=unitID)

        if student:
            student=student[0]
            existing_attendance = GetAttendance(input_sessionID=sessionID, studentID=studentID)

            if existing_attendance:
                flask.flash("User already signed in", category='error')
                return flask.redirect(flask.url_for('home'))
            
            consent_int = 1 if consent_status == "yes" else 0

            student.consent = consent_int
            db.session.commit()

            # Add attendance for the current session
            AddAttendance(sessionID=sessionID, studentID=studentID, consent_given=1, facilitatorID=1) # TODO need to be replaced with actual facilitator ID logic

            return flask.redirect(flask.url_for('home'))

        else:
            flask.flash(f"Invalid student information", 'error')

    # Redirect back to home page when done
    return flask.redirect(flask.url_for('home'))
    
@app.route('/student_suggestions', methods=['GET'])
def student_suggestions(): 
    # get the search query from the request
    query = flask.request.args.get('q', '').strip().lower()

    # TODO will need to be replaced with actual session logic later 
    current_session = GetSession(sessionID=1)[0] 

    # get students in the unit associated with the session
    students = GetStudent(unitID=current_session.unitID)

    # filter students based on the query (by name or student number)
    suggestions = []
    for student in students:
        existing_attendance = GetAttendance(input_sessionID=current_session.sessionID, studentID=student.studentID)

        if existing_attendance:
            continue

        first_last_name = f"{student.firstName} {student.lastName}"
        preferred_last_name = f"{student.preferredName} {student.lastName}"
        if query in student.lastName.lower() or query in student.preferredName.lower() or query in preferred_last_name.lower() or query in str(student.studentNumber):
            suggestions.append({
                'name': f"{student.preferredName} {student.lastName}",
                'id': student.studentID,
                'number': student.studentNumber
            })
        elif query in student.firstName.lower() or query in first_last_name.lower():
            suggestions.append({
                'name': f"{student.firstName} {student.lastName}",
                'id': student.studentID,
                'number': student.studentNumber
            })

    return flask.jsonify(suggestions)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return flask.redirect(flask.url_for('login'))

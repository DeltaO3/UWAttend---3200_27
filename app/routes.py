import flask

from app import app
from .forms import *
from .helpers import *
from .models import *
from .database import *
from .utilities import *
from app import database
from flask import send_file, redirect, url_for, after_this_request
from flask_login import current_user, login_user, logout_user, login_required
import os
from datetime import datetime, date
import sqlalchemy as sa

# HOME -   /home/
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
@login_required
def home():
    session_id = flask.session.get('session_id')

    current_session = GetSession(session_id) 
    
    if current_session:
        current_session = current_session[0]
        # Use session_id for further processing

    if not current_session:
        return redirect(url_for('session')) 

    form = StudentSignInForm()

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
            "photo": student.consent,
            "time": attendance_record.signInTime
        }
        student_list.append(student_info)

    student_list.sort(key=lambda x: x['time'], reverse=True)

    return flask.render_template('home.html', form=form, students=student_list, current_session=current_session, total_students=len(student_list), signed_in=signed_in_count, session_num=current_session.sessionID) 
	
# CONFIGURATION - /session/ /admin/
@app.route('/session', methods=['GET', 'POST'])
@login_required
def session():

    # if session already exists, redirect to /updatesession
    session_id = flask.session.get('session_id')
    existing_session = GetSession(session_id)
    if existing_session:
        return redirect(url_for('updatesession'))

    form = SessionForm()

    # Get perth time
    perth_time = get_perth_time()
    humanreadable_perth_time = perth_time.strftime('%B %d, %Y, %H:%M:%S %Z')

    # For JS formatting
    formatted_perth_time = perth_time.isoformat()

    if form.validate_on_submit():

        # Handle form submission
        unit_id = form.unit.data
        session_name = form.session_name.data
        session_time = form.session_time.data

        # Printing for debugging
        print(f"Session Name: {session_name}")
        print(f"Session Time: {session_time}")
        print(f"Unit Id: {unit_id}")
        print(f"Current Date/Time: {humanreadable_perth_time}")

        # Check if the session already exists
        current_session = GetUniqueSession(unit_id, session_name, session_time, perth_time.date())

        if current_session is not None :
            print("Session already exists.")
        else :
            print("Session doesn't exist... creating new session.")
            current_session = AddSession(unit_id, session_name, session_time, perth_time)
            if current_session is None :
                print("An error has occurred. The session was not created. Please try again.")
                return flask.redirect(flask.url_for('home'))

        print("Current session details:")
        print(f"Session name: {current_session.sessionName}")
        print(f"Session time: {current_session.sessionTime}")

        flask.session['session_id'] = current_session.sessionID
        print(f"Saving session id: {current_session.sessionID} to global variable")

        # Redirect back to home page with the session ID as a query parameter
        return flask.redirect(flask.url_for('home'))

    # set session form select field options
    set_session_form_select_options(form)

    return flask.render_template('session.html', form=form, perth_time=formatted_perth_time)

@app.route('/updatesession', methods=['GET', 'POST'])
def updatesession():

    # if session doesn't exist, redirect to /session
    session_id = flask.session.get('session_id')
    existing_session = GetSession(session_id)
    if not existing_session:
        return redirect(url_for('session'))

    form = SessionForm()

    perth_time = get_perth_time()

    # For JS formatting
    formatted_perth_time = perth_time.isoformat()

    if form.validate_on_submit():
        # Handle form submission
        unit_id = form.unit.data
        session_name = form.session_name.data
        session_time = form.session_time.data

        # Printing for debugging
        print(f"Session Name: {session_name}")
        print(f"Session Time: {session_time}")
        print(f"Unit Id: {unit_id}")

        # TODO: implement update session logic

    # set updatesession form select fields to match current session's details
    current_session = existing_session[0]
    current_unit = GetUnit(unitID=current_session.unitID)[0]
    set_updatesession_form_select_options(current_session, current_unit, form)

    return flask.render_template('updatesession.html', form=form, perth_time=formatted_perth_time)

#ADMIN - /unitconfig /
@app.route('/unitconfig', methods=['GET', 'POST'])
@login_required
def unitconfig():
    if current_user.userType == 'facilitator':
        return flask.redirect('home')
    
    return flask.render_template('unit.html')

# add users
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.userType != 'admin':
        return flask.redirect('home')

    form = AddUserForm()

    if form.validate_on_submit() and flask.request.method == 'POST':       
        
        AddUser(userType=form.UserType.data, uwaID=form.uwaId.data, firstName=form.firstName.data, lastName=form.lastName.data, passwordHash=form.passwordHash.data)
        return flask.redirect(flask.url_for('admin'))
    
    return flask.render_template('admin.html', form=form)

# ADDUNIT - /addunit/ /unit/
@app.route('/addunit', methods=['GET', 'POST'])
@login_required
def addunit():
    if current_user.userType == 'facilitator':
        return flask.redirect('home')
    
    form = AddUnitForm()

    if form.validate_on_submit() and flask.request.method == 'POST':
        #Form data held here
        newunit_code = form.unitcode.data
        unit_name = form.unitname.data
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

        #Validation occurs in flask forms with custom validators
        
        #convert session occurences to a | string
        occurences = ""
        for time in sessionoccurence:
            occurences += time + "|"
        occurences = occurences[:-1]
        print(f"session occurence string: {occurences}")

        #add to database
        unitID = AddUnit(newunit_code, unit_name, semester, start_date, end_date, 
                sessionnames, occurences, commentsenabled , assessmentcheck, consent_required, commentsuggestions )
        
         #read CSV file
        if student_file.filename != '':
            student_file.save(student_file.filename)
            filename = student_file.filename
            process_csv(filename, unitID)
        else:
            print("Submitted no file, probable error.")
            error = "No file submitted"
            return flask.render_template('addunit.html', form=form, error=error)
        
        #Handle facilitators
        #TODO: handle emailing facilitators, handle differentiating between facilitator and coordinator
        facilitator_emails = facilitator_list.split('|')
        for facilitator in facilitator_emails:
            if(not GetUser(email=facilitator)):
                print(f"Adding new user: {facilitator}")
                AddUser(facilitator, "placeholder", "placeholder", facilitator, 'facilitator') #Do we assign coordinators?
            #add this unit to facilitator
            if(facilitator == current_user.email):
                print(f"skipping user {facilitator} as it is the currently logged in user.")
                continue
            print(f"Adding unit {unitID} to facilitator {facilitator}")
            AddUnitToFacilitator(facilitator, unitID)
        AddUnitToFacilitator(current_user.email, unitID)
        AddUnitToCoordinator(current_user.email, unitID)
        
        return flask.redirect(flask.url_for('unitconfig'))
	    
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
    session_id = flask.session.get('session_id')
    print(f"Session ID as found in student : {session_id}")
    current_session = GetSession(sessionID=session_id)

    if not current_session:
        flask.flash("Error loading session") 
        return flask.redirect(flask.url_for('home'))
    
    current_session = current_session[0]

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
        "photo": "yes" if student.consent == "yes" else "no",
        "time": attendance_record.signInTime
    }

    return flask.render_template('student.html', student=student_info)
	
# LOGIN - /login/ 
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        print("authenticated")
        return flask.redirect('home')
    
    form = LoginForm()
    if form.validate_on_submit():
        user = database.GetUser(email = form.username.data)                

        if user is None or not user.is_password_correct(form.password.data):
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
        # sessionID = form.sessionID.data

        print(f'{studentID} consent as given in form: {consent_status}')

        session_id = flask.session.get('session_id')
        print("Session ID as found in add_student : ", session_id)

        session = GetSession(sessionID=session_id)

        if not session:
            flask.flash("Error loading session") 
            return flask.redirect(flask.url_for('home'))
        
        session = session[0]
        unitID = session.unitID
        
        student = GetStudent(studentID=studentID, unitID=unitID)

        if student:
            student=student[0]
            existing_attendance = GetAttendance(input_sessionID=session_id, studentID=studentID)
            
            if existing_attendance:
                flask.flash("User already signed in", category='error')
                return flask.redirect(flask.url_for('home'))
            
            # consent will be none if it is already yes or not required i.e. no changes required
            if consent_status != "none" :
                student.consent = "yes" if consent_status == "yes" else "no"

            print(f'{student.studentID} consent as added to db: {student.consent}')

            db.session.commit()

            # Add attendance for the current session
            AddAttendance(sessionID=session_id, studentID=studentID, consent_given=student.consent, facilitatorID=1) # TODO need to be replaced with actual facilitator ID logic
            print(f"Logged {student.firstName} {student.lastName} in")

            return flask.redirect(flask.url_for('home'))

        else:
            flask.flash(f"Invalid student information", 'error')

    # Redirect back to home page when done
    return flask.redirect(flask.url_for('home'))

@app.route('/get_session_details/<unitID>')
def get_session_details(unitID) :

    # get unit by unitID
    unit = GetUnit(unitID=unitID)
    
    # get session names for unit
    session_names = unit[0].sessionNames.split('|')
    session_name_choices = []

    for name in session_names :
        session_name_choices.append(name)

    # get session times for unit
    session_times = unit[0].sessionTimes.split('|')
    session_time_choices = []

    for time in session_times :
        session_time_choices.append(time)

    print(f"Sending session details for {unit[0].unitCode}")

    # send session details
    return flask.jsonify({'session_name_choices': session_name_choices, 'session_time_choices': session_time_choices})

@app.route('/student_suggestions', methods=['GET'])
def student_suggestions(): 
    # get the search query from the request
    query = flask.request.args.get('q', '').strip().lower()

    # TODO will need to be replaced with actual session logic later 
    session_id = flask.session.get('session_id')
    current_session = GetSession(sessionID=session_id)[0] 

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
                'number': student.studentNumber,
                'consentNeeded': student.consent
            })
        elif query in student.firstName.lower() or query in first_last_name.lower():
            suggestions.append({
                'name': f"{student.firstName} {student.lastName}",
                'id': student.studentID,
                'number': student.studentNumber,
                'consentNeeded': student.consent
            })

    return flask.jsonify(suggestions)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return flask.redirect(flask.url_for('login'))

@app.route('/sign_all_out', methods=['POST'])
def sign_all_out():
    session_id = flask.session.get('session_id')

    session = GetSession(sessionID=session_id)
    if not session:
        flask.flash('Failed to sign out all users - invalid session key')

    attendance_records = GetAttendance(input_sessionID=session_id)
    if not attendance_records:
        flask.flash('Failed to sign out all users - no users signed in')

    current_time = get_perth_time().time() # did this so that they all have an identical sign out time
    
    for record in attendance_records:
        if not record.signOutTime:
            record.signOutTime = current_time

    db.session.commit()
        

    print("Successfully signed out all users")
    return flask.redirect(flask.url_for('home'))

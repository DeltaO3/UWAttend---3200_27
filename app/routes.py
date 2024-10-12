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
    students = GetStudentList(student_ids=logged_in_student_ids) 

    student_list = []
    facilitator_list = []
    signed_in_count = 0

    for student in students:
        # find the student's attendance record 
        attendance_record = next((record for record in attendance_records if record.studentID == student.studentID), None)

        facilitator_id = attendance_record.facilitatorID
        if facilitator_id not in facilitator_list:
            facilitator_list.append(facilitator_id)

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

    student_list.sort(key=lambda x: (x['login'] == "yes", x['time']), reverse=True)


    # check if consent is required
    consent_required = GetUnit(unitID=current_session.unitID)[0].consent
    
    return flask.render_template('home.html', form=form, students=student_list, current_session=current_session, total_students=len(student_list), signed_in=signed_in_count, session_num=current_session.sessionID, consent_required=consent_required, num_facilitators=len(facilitator_list)) 
	
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

    if flask.request.method == 'POST' :
        if form.validate_on_submit():

            # Handle form submission
            unit_id = form.unit.data
            session_name = form.session_name.data
            session_time = form.session_time.data
            session_date = form.session_date.data

            # Printing for debugging
            print(f"Session Name: {session_name}")
            print(f"Session Time: {session_time}")
            print(f"Unit Id: {unit_id}")
            print(f"Session Date: {session_date}")

            # Check if the session already exists
            current_session = GetUniqueSession(unit_id, session_name, session_time, session_date)

            if current_session is not None :
                print("Session already exists.")
            else :
                print("Session doesn't exist... creating new session.")
                current_session = AddSession(unit_id, session_name, session_time, session_date)
                if current_session is None :
                    print("An error has occurred. The session was not created. Please try again.")
                    return flask.redirect(flask.url_for('home'))

            print("Current session details:")
            print(f"Session name: {current_session.sessionName}")
            print(f"Session time: {current_session.sessionTime}")
            print(f"Session date: {current_session.sessionDate}")

            flask.session['session_id'] = current_session.sessionID
            print(f"Saving session id: {current_session.sessionID} to global variable")

            # Redirect back to home page with the session ID as a query parameter
            return flask.redirect(flask.url_for('home'))
        else :
            set_session_form_select_options(form)
            return flask.render_template('session.html', form=form, perth_time=formatted_perth_time, update=False, errorMsg="Please select a valid option for all fields.")

    # set session form select field options
    set_session_form_select_options(form)
    return flask.render_template('session.html', form=form, perth_time=formatted_perth_time, update=False)

@app.route('/updatesession', methods=['GET', 'POST'])
@login_required
def updatesession():

    # if session doesn't exist, redirect to /session
    current_session_id = flask.session.get('session_id')
    existing_session = GetSession(current_session_id)
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
        session_date = form.session_date.data

        # Printing for debugging
        print(f"Session Name: {session_name}")
        print(f"Session Time: {session_time}")
        print(f"Session Date: {session_date}")
        print(f"Unit Id: {unit_id}")

        # Check if the session already exists
        new_session = GetUniqueSession(unit_id, session_name, session_time, session_date)

        if new_session is not None :
            print("Session already exists. Joining existing session.")
        else :
            print("Session doesn't exist... creating new session with new details.")
            new_session = AddSession(unit_id, session_name, session_time, session_date)
            if new_session is None :
                print("An error has occurred. The session was not created. Please try again.")
                return flask.redirect(flask.url_for('home'))

        print("New session details:")
        print(f"Session name: {new_session.sessionName}")
        print(f"Session time: {new_session.sessionTime}")
        print(f"Session date: {new_session.sessionDate}")

        # Update attendance records with current session id and where facilitator is current user
        attendance_records = GetAttendanceByIDAndFacilitator(current_session_id, current_user.userID)

        for record in attendance_records :
            record.sessionID = new_session.sessionID

        db.session.commit()

        # Update session cookie
        flask.session['session_id'] = new_session.sessionID
        print(f"Saving session id: {new_session.sessionID} to global variable")

        # Redirect back to home page
        return flask.redirect(flask.url_for('home'))

    # set updatesession form select fields to match current session's details
    current_session = existing_session[0]
    current_unit = GetUnit(unitID=current_session.unitID)[0]
    set_updatesession_form_select_options(current_session, current_unit, form)

    return flask.render_template('session.html', form=form, perth_time=formatted_perth_time, update=True, currentSession=current_session, unit=current_unit.unitCode)

@app.route('/checksessionexists', methods=['POST'])
@login_required
def checksessionexists():
    form = SessionForm()

    if form.validate_on_submit():
        # Handle form submission
        unit_id = form.unit.data
        session_name = form.session_name.data
        session_time = form.session_time.data
        session_date = form.session_date.data

        print(f"Session Name: {session_name}")
        print(f"Session Time: {session_time}")
        print(f"Session Date: {session_date}")
        print(f"Unit Id: {unit_id}")

        # Check if the session already exists
        new_session = GetUniqueSession(unit_id, session_name, session_time, session_date)

        if new_session is not None :
            print("Session already exists. Joining existing session.")
            facilitatorNames = GetFacilitatorNamesForSession(new_session.sessionID)
            for f in facilitatorNames :
                print(f)
            return flask.jsonify({'sessionExists': "true", 'facilitatorNames': facilitatorNames})
        
        else :
            print("Session doesn't exist.")
            return flask.jsonify({'sessionExists': "false", })

#ADMIN - /unitconfig /
@app.route('/unitconfig', methods=['GET', 'POST'])
@login_required
def unitconfig():
    if current_user.userType == 'facilitator':
        return flask.redirect('home')
    
    units_list = current_user.unitsCoordinate

    # Create a list to hold unit information
    units_data = []

    for unit in units_list:
        # Extract relevant data for each unit
        unit_info = {
            "code": unit.unitCode,
            "name": unit.unitName or "N/A",
            "study_period": unit.studyPeriod,
            "start_date": unit.startDate.strftime('%Y-%m-%d'),
            "end_date": unit.endDate.strftime('%Y-%m-%d'),
            "unit_id": str(unit.unitID)
        }
        units_data.append(unit_info)
    
    return flask.render_template('unit.html', units=units_data)

#UPDATE UNIT FORM
@app.route('/updateunit', methods=['GET', 'POST'])
@login_required
def updateunit():
    if current_user.userType == 'facilitator':
        return flask.redirect('home')
    
    if 'id' not in flask.request.args:
        return flask.redirect('unitconfig')
    
    unit_id = flask.request.args.get('id') 
    unit_data = GetUnit(unitID=unit_id)
    if not unit_data:
        flask.flash("Unit not found", "error")
        return flask.redirect(flask.url_for('unitconfig'))
    unit = unit_data[0]  
    if unit not in current_user.unitsCoordinate: #!!! TEST THIS WORKS AS INTENDED (cant access not your own units)
        flask.flash("Unit not found", "error") #Saying that the ID exists is a vulnerability, so we just say it doesnt
        return flask.redirect(flask.url_for('unitconfig'))
    
    #Hardcoding unit session times conversion:
    session_occurence_name = ""
    if unit.sessionTimes == "Morning|Afternoon":
        session_occurence_name = "Morning/Afternoon"
    else:
        session_occurence_name = "Hours"
    print(session_occurence_name)

    # Initialize the form with the existing unit data as defaults
    if flask.request.method != 'POST':
        form = UpdateUnitForm(
            unitcode=unit.unitCode,
            currentUnit = unit.unitCode,
            unitname=unit.unitName,
            semester=unit.studyPeriod,
            startdate=unit.startDate,
            currentUnitStart = unit.startDate,
            enddate=unit.endDate,
            sessions=unit.sessionNames,
            commentsenabled=unit.comments,
            assessmentcheck=unit.marks,
            consentcheck=unit.consent,
            comments=unit.commentSuggestions,
            sessionoccurence = session_occurence_name
        )
    else:
        form = UpdateUnitForm()

    if form.validate_on_submit() and flask.request.method == 'POST':
        # Update unit variables from update unit form
        unitCode = form.unitcode.data
        unitName = form.unitname.data
        studyPeriod = form.semester.data
        startDate = form.startdate.data
        endDate = form.enddate.data
        sessionNames = form.sessions.data
        comments = form.commentsenabled.data
        marks = form.assessmentcheck.data
        consent = form.consentcheck.data
        commentSuggestions = form.comments.data
        sessionoccurence = form.sessionoccurence.data

        print(sessionoccurence)

        #convert session occurences to a | string
        occurences = ""
        if sessionoccurence == "Morning/Afternoon":
            occurences = "Morning|Afternoon"
        elif sessionoccurence == "Hours":
            occurences = "8am|9am|10am|11am|12pm|1pm|2pm|3pm|4pm|5pm|6pm"
        else:
            print("No occurence, probable error")
            flask.flash("Error with session occurence", 'error')
            return flask.render_template('addunit.html', form=form)
        print(f"session occurences: {occurences}")
        
        print(f"Updating unit ID: {unit_id}, Code: {unitCode}, Name: {unitName}")

        # Update the unit's database record with the new form data
        EditUnit(
            unit_id,
            unitCode,
            unitName,
            studyPeriod,
            startDate,
            endDate,
            sessionNames,
            occurences,
            comments,
            marks,
            consent,
            commentSuggestions
        )

        flask.flash("Unit updated successfully", "success")
        return flask.redirect(flask.url_for('unitconfig'))

    return flask.render_template('addunit.html', form=form, edit=True, unit_id = unit_id)

@app.route('/editStudents', methods=['GET', 'POST'])
@login_required
def editStudents():
    unit_id = flask.request.args.get('id')
    unit = GetUnit(unitID=unit_id)[0]
    form = AddStudentForm()
    csv_form = UploadStudentForm()

    if form.submit.data and form.validate_on_submit() and flask.request.method == 'POST':
        consent = "not required" if unit.consent == False else "no"
        #Ensure you cant add duplicate students
        if GetStudent(unitID=unit_id, studentNumber=form.studentNumber.data)[0] is None:
            flask.flash("Student already assigned to this unit", "error")
            return flask.redirect(url_for('editStudents', id=unit_id))
        AddStudent(form.studentNumber.data, form.firstName.data, form.lastName.data, form.title.data, form.preferredName.data, unit_id, consent)
        flask.flash("Student added successfully", "success")
        return flask.redirect(url_for('editStudents', id=unit_id))

    students = GetStudent(unitID = unit_id)
    student_list = []
    for student in students:
        student_info = {
            "name": f"{student.preferredName} {student.lastName}",
            "number": student.studentNumber,
            "id": str(student.studentID),
        }
        student_list.append(student_info)
    
    
    return flask.render_template('editPeople.html', unit_id=str(unit_id), type="students", students=student_list, unit=unit, form=form, csv_form = csv_form)

@app.route('/uploadStudents', methods=['POST'])
@login_required
def uploadStudents():
    csv_form = UploadStudentForm()
    unit_id = flask.request.args.get('id')

    if csv_form.validate_on_submit():
        student_file = csv_form.studentfile.data
        if student_file.filename != '':
            student_filename = f"{unit_id}_new_students.csv"
            student_file.save(student_filename)
            print(f"Student filename: {student_filename}")
        else:
            print("Submitted no file, probable error.")
            flask.flash("Error, no student file submitted", 'error')
            return flask.redirect(url_for('editStudents', id=unit_id))
        s_data, error = process_csvs(student_filename, None)
        if os.path.exists(student_filename):
            os.remove(student_filename)
        if error:
            flask.flash(error, 'error')
            return flask.redirect(url_for('editStudents', id=unit_id))
        import_student_in_db(s_data, unit_id)
        flask.flash("Added students to DB", "success")
        return flask.redirect(url_for('editStudents', id=unit_id))
    else:
        flask.flash("Error uploading CSV file", 'error')
        return flask.redirect(url_for('editStudents', id=unit_id))

@app.route('/deleteStudent', methods=['POST'])
@login_required
def deleteStudent():
    unit_id = flask.request.args.get('unit_id')
    unit = GetUnit(unitID=unit_id)[0]
    if unit not in current_user.unitsCoordinate: #!check this works
        flask.flash("Unit not found","error")
        return flask.redirect(url_for('unitconfig'))

    student_id = flask.request.args.get('student_id')
    if deleteStudentFromDB(unit_id, student_id):
        flask.flash("Student deleted successfully","success")
        return flask.redirect(url_for('editStudents', id=unit_id))
    
    flask.flash("Error deleting student", "error")
    return flask.redirect(url_for('editStudents', id=unit_id))

@app.route('/editFacilitators', methods=['GET', 'POST'])
@login_required
def editFacilitators():
    unit_id = flask.request.args.get('id')
    unit = GetUnit(unitID=unit_id)[0]
    facilitators = GetUnit(unitID=unit_id)[0].facilitators
    facilitator_list = []

    for facilitator in facilitators:
        info = {
            "name": f"{facilitator.firstName} {facilitator.lastName}",
            "email": facilitator.email,
        }
        facilitator_list.append(info)
    #facilitators = GetStudent(unitID = unit_id)
    return flask.render_template('editPeople.html', unit_id=str(unit_id), unit=unit, type="facilitators", facilitators=facilitator_list)

@app.route('/deleteFacilitator', methods=['POST'])
@login_required
def deleteFacilitator():
    unit_id = flask.request.args.get('unit_id')
    unit = GetUnit(unitID=unit_id)[0]
    if unit not in current_user.unitsCoordinate: #!check this works
        flask.flash("Unit not found","error")
        return flask.redirect(url_for('unitconfig'))
    
    facilitator_email = flask.request.args.get('facilitator_id')
    if deleteFacilitatorConnection(unit_id, facilitator_email):
        flask.flash("Facilitator deleted successfully","success")
        return flask.redirect(url_for('editFacilitators', id=unit_id))
    
    flask.flash("Error deleting facilitator", "error")
    return flask.redirect(url_for('editFacilitators', id=unit_id))



# add users
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.userType != 'admin':
        return flask.redirect('home')

    form = AddUserForm()

    if form.validate_on_submit() and flask.request.method == 'POST':       
        
        AddUser(userType=form.UserType.data, email=form.email.data, firstName=form.firstName.data, lastName=form.lastName.data, passwordHash=form.passwordHash.data)
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
        facilitator_file = form.facilitatorfile.data
        sessionnames = form.sessions.data
        sessionoccurence = form.sessionoccurence.data 
        assessmentcheck = form.assessmentcheck.data
        commentsenabled = form.commentsenabled.data
        commentsuggestions = form.comments.data 

        print(f"session string: " + sessionnames + "; commentString: " + commentsuggestions) #Checking hidden form works

        #Validation occurs in flask forms with custom validators
        
        #convert session occurences to a | string
        occurences = ""
        if sessionoccurence == "Morning/Afternoon":
            occurences = "Morning|Afternoon"
        elif sessionoccurence == "Hours":
            occurences = "8am|9am|10am|11am|12pm|1pm|2pm|3pm|4pm|5pm|6pm"
        else:
            print("No occurence, probable error")
            flask.flash("Error with session occurence", 'error')
            return flask.render_template('addunit.html', form=form)
        print(f"session occurence string: {occurences}")

         #read CSV file
        if student_file.filename != '':
            student_filename = f"{newunit_code}_students.csv"
            student_file.save(student_filename)
            print(f"Student filename: {student_filename}")
        else:
            print("Submitted no file, probable error.")
            flask.flash("Error, no student file submitted", 'error')
            return flask.render_template('addunit.html', form=form)
        
        if facilitator_file.filename != '':
            facilitator_filename = f"{newunit_code}_facilitators.csv"
            facilitator_file.save(facilitator_filename)
            print(f"Facilitator filename: {facilitator_filename}")
        else:
            print("Submitted no file, probable error.")
            flask.flash("Error, no facilitator file submitted", 'error')
            return flask.render_template('addunit.html', form=form)
     
        #Process csvs
        s_data, f_data, error = process_csvs(student_filename, facilitator_filename)

        if os.path.exists(student_filename):
            os.remove(student_filename)
        if os.path.exists(facilitator_filename):
            os.remove(facilitator_filename)
        if error:
            flask.flash(error, 'error')
            return flask.render_template('addunit.html', form=form)
        
        #add to database
        unit_id = AddUnit(newunit_code, unit_name, semester, start_date, end_date, 
                sessionnames, occurences, commentsenabled , assessmentcheck, consent_required, commentsuggestions )
        
        #Add from csv
        #TODO: handle emailing facilitators - should go in the correct process csv function
        import_student_in_db(s_data, unit_id)
        import_facilitator_in_db(f_data, unit_id, current_user)
        
        AddUnitToFacilitator(current_user.email, unit_id)
        AddUnitToCoordinator(current_user.email, unit_id)
        
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
@login_required
def student():
    form = AttendanceChangesForm()

    student_id = flask.request.form['student_id']

    student = GetStudent(studentID=student_id)

    if not student:
        flask.flash("Error - Student not found")
        return flask.redirect(flask.url_for('home'))
    
    student = student[0]

    session_id = flask.session.get('session_id')
    print(f"Session ID as found in student : {session_id}")
    current_session = GetSession(sessionID=session_id)

    if not current_session:
        flask.flash("Error loading session") 
        return flask.redirect(flask.url_for('home'))
    
    current_session = current_session[0]

    unit = GetUnit(unitID=current_session.unitID)

    if not unit:
        flask.flash("Error loading unit") 
        return flask.redirect(flask.url_for('home'))
    
    unit = unit[0]
    comment_suggestions = unit.commentSuggestions
    comment_list = comment_suggestions.split('|')

    attendance_record = GetAttendance(input_sessionID=current_session.sessionID, studentID=student_id)[0] 

    student_info = generate_student_info(student, attendance_record)
    print("comments", student_info["comments"])
    print("consent", student.consent)

    # check if consent, comments and marks are required
    consent_required = GetUnit(unitID=current_session.unitID)[0].consent
    marks_enabled = GetUnit(unitID=current_session.unitID)[0].marks
    comments_enabled = GetUnit(unitID=current_session.unitID)[0].comments
    comments_label = form.comments.label.text

    if not comments_enabled :
       comments_label = "Multiple sign in/out time log"

    return flask.render_template('student.html', form=form, student=student_info, attendance=attendance_record, consent_required=consent_required, comments_enabled=comments_enabled, marks_enabled=marks_enabled, comments_label=comments_label)

@app.route('/remove_from_session', methods=['GET'])
@login_required
def remove_from_session():
    # Access form data
    student_id = flask.request.args.get('student_id')

    session = flask.session.get('session_id')

    current_session = GetSession(session)

    if not current_session:
        flask.flash("Error loading session") 
        return flask.redirect(flask.url_for('home'))
    
    current_session = current_session[0]

    status = RemoveStudentFromSession(student_id, current_session.sessionID)

    if status:
        flask.flash("Student removed from session")
    else:
        flask.flash("Error removing student from session")
        
    return flask.redirect(flask.url_for('home'))

# CREATE ACCOUNT - /create_account
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if current_user.is_authenticated:
        return flask.redirect('home')
    
    form = CreateAccountForm()
    if form.validate_on_submit():
        #TODO: Add email logic
        #Uses a placeholder email - perhaps this should be included in the route as a ?email=email parameter?
        #feels unsafe, feel free to change some things. 
        email = form.firstName.data + "@placeholder.com"
        AddUser(email, form.firstName.data, form.lastName.data, form.password2.data, "facilitator" )
        print(f"Added user" + form.firstName.data)
        login_user(GetUser(email = email))
        return flask.redirect(flask.url_for('home'))
    
    return flask.render_template('createAccount.html', form=form)

#FORGOT PASSWORD - /forgot_password
@app.route('/forgot_password', methods=['GET'])
def forgot_password():
    if current_user.is_authenticated:
        return flask.redirect('home')
    #TODO: add backend logic for email
    return flask.render_template('forgotPassword.html')

#RESET PASSWORD - /reset_password
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return flask.redirect('home')
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #TODO: add email into logic (similar to what create account does)
        print("resetting password...")
        SetPassword("admin@admin.com", form.password2.data)
        flask.flash('Password changed successfully', category="success")
        return flask.redirect(flask.url_for('login'))

    return flask.render_template('resetPassword.html', form=form)


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
            flask.flash('Invalid username or password', category="error")
            return flask.redirect('login')
        
        login_user(user, remember=form.remember_me.data)
        return flask.redirect('home')

    return flask.render_template('login.html', form=form)

@app.route('/edit_student_details', methods=['POST'])
@login_required
def edit_student_details():

    form = AttendanceChangesForm()

    session = flask.session.get('session_id')

    current_session = GetSession(session)

    if not current_session:
        flask.flash("Error loading session") 
        return flask.redirect(flask.url_for('home'))
    
    current_session = current_session[0]

    if form.validate_on_submit():

        # Build the dictionary with only non-empty/None values
        update_data = { 
            'sessionID': current_session.sessionID,
            'studentID': form.student_id.data,
            'signInTime': form.signInTime.data or None,
            'signOutTime': form.signOutTime.data or None,
            'login': form.login.data if form.login.data is not None else None,
            'consent': form.consent.data if form.consent.data is not None else None,
            'grade': form.grade.data or None,
            'comments': form.comments.data or None
        }

        # Remove keys with None values to pass only filled data
        update_data = {k: v for k, v in update_data.items() if v is not None}

        if update_data:
            message = EditAttendance(**update_data)   

            if message == "True":
                flask.flash("Student details updated", category='success')
            else:
                flask.flash(message, category='error')
                student = GetStudent(studentID=form.student_id.data)
                attendance_record = GetAttendance(input_sessionID=current_session.sessionID, studentID=form.student_id.data)
                print(form.student_id.data)
                if not student or not attendance_record:
                    return flask.redirect(flask.url_for('home'))
                return flask.render_template('student.html', form=form, student=generate_student_info(student[0], attendance_record[0]), attendance=attendance_record[0])

    return flask.redirect(flask.url_for('home'))

@app.route('/add_student', methods=['POST'])
@login_required
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
                if not existing_attendance[0].signOutTime:
                    status = SignStudentOut(attendanceID=existing_attendance[0].attendanceID)
                    if status:
                        flask.flash(f"Signed out {student.preferredName} {student.lastName}", 'success')
                    else:
                        flask.flash(f"Error signing out {student.preferredName} {student.lastName}", 'error')
                else:
                    status = RemoveSignOutTime(attendanceID=existing_attendance[0].attendanceID)
                return flask.redirect(flask.url_for('home'))
            
            # consent will be none if it is already yes or not required i.e. no changes required
            if consent_status != "none" :
                student.consent = "yes" if consent_status == "yes" else "no"

            unit = GetUnit(unitID=unitID)

            if not unit :
                flask.flash("Error loading unit details")
                return flask.redirect(flask.url_for('home'))
            
            unit = unit[0]

            if not unit.consent :
                student.consent = "not required"

            # Add attendance for the current session
            AddAttendance(sessionID=session_id, studentID=studentID, consent_given=student.consent, facilitatorID=current_user.userID)
            print(f"Logged {student.preferredName} {student.lastName} in")

            return flask.redirect(flask.url_for('home'))

        else:
            flask.flash("Invalid student information", 'error')

    # Redirect back to home page when done
    return flask.redirect(flask.url_for('home'))

@app.route('/get_session_details/<unitID>')
@login_required
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

    session_time_default = get_time_suggestion(session_times) 

    if session_time_default is None :
        session_time_default = '--Select--'

    for time in session_times :
        session_time_choices.append(time)

    print(f"Sending session details for {unit[0].unitCode}")

    print(f"session time default: {session_time_default}")

    # send session details
    return flask.jsonify({'session_name_choices': session_name_choices, 'session_time_choices': session_time_choices, 'session_time_default': session_time_default})

@app.route('/student_suggestions', methods=['GET'])
@login_required
def student_suggestions(): 
    # get the search query from the request
    query = flask.request.args.get('q', '').strip().lower()

    # TODO will need to be replaced with actual session logic later 
    session_id = flask.session.get('session_id')
    current_session = GetSession(sessionID=session_id)[0] 
    unit = GetUnit(unitID=current_session.unitID)[0]
    print(unit.consent)

    # get students in the unit associated with the session
    students = GetStudent(unitID=current_session.unitID)

    # filter students based on the query (by name or student number)
    suggestions = []
    for student in students:
        existing_attendance = GetAttendance(input_sessionID=current_session.sessionID, studentID=student.studentID)

        first_last_name = f"{student.firstName} {student.lastName}"
        preferred_last_name = f"{student.preferredName} {student.lastName}"
        if query in student.lastName.lower() or query in student.preferredName.lower() or query in preferred_last_name.lower() or query in str(student.studentNumber):
            consent = student.consent
            if existing_attendance:
                consent = "yes"
            if not unit.consent:
                consent = "not required"
            signedIn = 0 
            if existing_attendance:
                if not existing_attendance[0].signOutTime:
                    signedIn = 1
            suggestions.append({
                'name': f"{student.preferredName} {student.lastName}",
                'id': student.studentID,
                'number': student.studentNumber,
                'consentNeeded': consent,
                'signedIn': signedIn,
            })
        elif query in student.firstName.lower() or query in first_last_name.lower():
            consent = student.consent
            if existing_attendance:
                consent = "yes"
            if not unit.consent:
                consent = "not required"
            signedIn = 0 
            if existing_attendance:
                if not existing_attendance[0].signOutTime:
                    signedIn = 1
            suggestions.append({
                'name': f"{student.firstName} {student.lastName}",
                'id': student.studentID,
                'number': student.studentNumber,
                'consentNeeded': consent,
                'signedIn': signedIn,
            })

    return flask.jsonify(suggestions)

@app.route('/logout')
@login_required
def logout():
    removeSessionCookie()
    logout_user()
    return flask.redirect(flask.url_for('login'))

@app.route('/sign_all_out', methods=['POST'])
@login_required
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

@app.route('/download_facilitator_template')
def download_facilitator_template():
    print("Sending facilitator template")
    # Serve the facilitator template from the static folder or any desired directory
    return flask.send_from_directory('static/files', 'facilitator_template.csv', as_attachment=True)

@app.route('/download_student_template')
def download_student_template():
    print("Sending student template")
    # Serve the student template from the static folder or any desired directory
    return flask.send_from_directory('static/files', 'student_template.csv', as_attachment=True)

@app.route('/ping')
def check_status():
    return "OK"

@app.route('/exitSession', methods=['GET'])
@login_required
def exitSession():
    removeSessionCookie()
    return flask.redirect(url_for('session'))


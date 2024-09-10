import flask
from datetime import datetime

from app import app
from .forms import LoginForm, SessionForm, StudentSignInForm
from .utilities import get_perth_time
from .models import db, Student, Session, Attendance
from .database import GetStudent, AddAttendance, GetSession

# HOME -   /home/
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():

    form = StudentSignInForm()

    # will need to be replaced with actual session logic later 
    current_session = db.session.query(Session).filter_by(sessionID=1).first()  

    print("session id (should be 1)", current_session.sessionID)

    # get students who have signed in for this session
    attendance_records = db.session.query(Attendance).filter_by(sessionID=current_session.sessionID).all()

    print("attendance records", attendance_records)

    # get student IDs from the attendance records
    logged_in_student_ids = [str(record.studentID) for record in attendance_records]

    print("logged in student ids", logged_in_student_ids)
    # print(type(logged_in_student_ids[0]))

    # get only the students who have logged in
    students = db.session.query(Student).filter(Student.studentID.in_(logged_in_student_ids)).all()

    print("students", students)

    student_list = []
    signed_in_count = 0

    for student in students:
        
        # find the student's attendance record 
        attendance_record = next((record for record in attendance_records if record.studentID == student.studentID), None)

        # set login status based on whether the student has a time marked where they logged out
        login_status = "no" if attendance_record.signOutTime else "yes"

        signed_in_count = signed_in_count + 1 if login_status == "yes" else signed_in_count

        print("consent", student.consent)

        student_info = {
            "name": f"{student.preferredName} {student.lastName}",
            "id": student.studentNumber,
            "login": login_status,  
            "photo": "yes" if student.consent == 1 else "no" 
        }
        student_list.append(student_info)

    return flask.render_template('home.html', form=form, students=student_list, session=current_session, total_students=len(student_list), signed_in=signed_in_count, session_num=1)
	
# CONFIGURATION - /session/ /admin/
@app.route('/session', methods=['GET', 'POST'])
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

@app.route('/admin', methods=['GET'])
def admin():
    return flask.render_template('admin.html')

# STUDENT - /student/
@app.route('/student', methods=['GET'])
def student():
    alex = {
        "name": "alex",
        "id": "12345678",
        "login": "yes",
        "photo": "no"
    }
    return flask.render_template('student.html', student=alex)
	
# LOGIN - /login/ 
@app.route('/login', methods=['GET', 'POST'])
def login():
    # placeholder values for testing
    test_username = "u1"
    test_password = "p1"

    form = LoginForm()

    if flask.request.method == 'POST' and form.validate_on_submit() :
        if form.username.data == test_username and form.password.data == test_password :
            return(flask.redirect(flask.url_for('session')))

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
    form = StudentSignInForm()
    print("here")

    if form.validate_on_submit():
        # Handle form submission
        studentID = form.studentID.data
        consent_status = form.consent_status.data
        sessionID = form.session_id.data

        # Printing for debugging
        print(f"Student ID: {studentID}")
        print(f"Consent Status: {consent_status}")
        print(f"Session ID: {sessionID}")

        # Update student info in database (login/consent)
        # student = GetStudent(studentID=int(studentID))
        
        student = db.session.query(Student).filter_by(studentID=int(studentID)).first()

        # TODO add check for if student is already signed in

        print(student)
        if student:
            consent_int = 1 if consent_status == "yes" else 0

            student.consent = consent_int
            db.session.commit()

            # Add attendance for the current session
            AddAttendance(attendanceID=None, sessionID=sessionID, studentID=studentID, consent_given=1, facilitatorID=1)
            print(f"Student {studentID} consent status updated to {consent_status}")

            return flask.redirect(flask.url_for('home'))

        else:
            print(f"No student found with ID {studentID}")

    # Redirect back to home page when done
    return flask.redirect(flask.url_for('home'))
    
@app.route('/student_suggestions', methods=['GET'])
def student_suggestions():
    # get the search query from the request
    query = flask.request.args.get('q', '').strip().lower()

    # will need to be replaced with actual session logic later 
    current_session = GetSession(sessionID=1)[0]  # 

    # get students in the unit associated with the session
    students = GetStudent(unitID=current_session.unitID)

    # filter students based on the query (by name or student number)
    suggestions = []
    for student in students:
        if query in student.firstName.lower() or query in student.lastName.lower() or query in student.preferredName.lower() or query in str(student.studentNumber):
            suggestions.append({
                'name': f"{student.preferredName} {student.lastName}",
                'id': student.studentID,
                'number': student.studentNumber
            })

    return flask.jsonify(suggestions)

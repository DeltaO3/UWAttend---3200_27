import flask
from datetime import datetime
from app import app
from app.forms import LoginForm, SessionForm, StudentSignInForm
from app.utilities import get_perth_time

# HOME -   /home/
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():

    form = StudentSignInForm()
    
    #placeholder data for table
    students = []
    alex = {
        "name": "alex",
        "id": "12345678",
        "login": "yes",
        "photo": "yes"
    }
    bob = {
        "name": "bob",
        "id": "87654321",
        "login": "no",
        "photo": "yes"
    }
    cathy = {
        "name": "cathy",
        "id": "22224444",
        "login": "yes",
        "photo": "no"
    }
    
    students.append(alex)
    students.append(bob)
    students.append(cathy)
    return flask.render_template('home.html', form=form, students=students)
	
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
@app.route('/student', methods=['GET', 'POST'])
def student():
    alex = {
        "name": "alex",
        "id": "12345678",
        "login": "yes",
        "photo": "no"
    }

    attendance = {
        "signInDate": "2022-01-01", 
        "signInTime": "09:01:27",
        "signOutDate": "2022-01-01",
        "signOutTime": "10:54:33",
        "studentID": "12345678",
    }
    return flask.render_template('student.html', student=alex, attendance=attendance)

@app.route('/remove_from_session', methods=['POST'])
def remove_from_session():
    # Access form data
    student_id = flask.request.form.get('student_id')
    print("Student ID: " + student_id)
    return flask.redirect('home')
	
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

    if form.validate_on_submit():
        # Handle form submission
        student_name = form.student_sign_in.data
        consent_status = form.consent_status.data

        # Printing for debugging
        print(f"Student Name: {student_name}")
        print(f"Consent Status: {consent_status}")

        # Update student info in database (login/consent)

        # Redirect back to home page when done
        return flask.redirect(flask.url_for('home'))

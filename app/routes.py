import flask
from app import app
from datetime import datetime




# HOME -   /home/
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return flask.render_template('home.html')
	
# CONFIGURATION - /session/ /admin/
@app.route('/session', methods=['GET', 'POST'])
def session():
    if flask.request.method == 'POST':
        # Handle form submission
        session_name = flask.request.form.get('session_name')
        unit_code = flask.request.form.get('unit_code')
        semester = flask.request.form.get('semester')
        session_time = flask.request.form.get('session_time')
        current_year = datetime.now().year

        # Create Database
        database_name = f"{unit_code}_{semester}_{current_year}"

        # Printing for debugging
        print(f"Session Name: {session_name}")
        print(f"Unit Code: {unit_code}")
        print(f"Semester: {semester}")
        print(f"Submitted Time: {session_time}")
        print(f"Database Name: {database_name}")

        # Redirect back to home page when done
        return flask.redirect(flask.url_for('home'))

    # Placeholder options for now. Replace these with info from the database
    placeholder_sessions = ["Safety", "CAD", "Computer", "PipeWorks", "Measurement", "ReverseEng", "DataMapping", "Soldering", "HandTools"]
    placeholder_unit_codes = ["GENG200", "CITS3007"]
    placeholder_semesters = ["SEM1", "SEM2"]

    return flask.render_template('session.html', sessions=placeholder_sessions, unit_codes=placeholder_unit_codes, semesters=placeholder_semesters)

@app.route('/admin', methods=['GET'])
def admin():
    return flask.render_template('admin.html')

# STUDENT - /student/
@app.route('/student', methods=['GET'])
def student():
    return flask.render_template('student.html')
	
# LOGIN - /login/ 
@app.route('/login', methods=['GET'])
def login():
    return flask.render_template('login.html')

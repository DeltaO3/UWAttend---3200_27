import flask
from datetime import datetime
from app import app
from app.forms import LoginForm
from app.forms import SessionForm
import sqlite3

global_unit_code = ""
global_UserId =0

# HOME -   /home/
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():

    global global_unit_code
    connect = sqlite3.connect("app\\Attendance.db")
    cursor = connect.cursor()
    print(global_unit_code)
    cursor.execute("SELECT * FROM attendance WHERE DateTime > datetime('now','-3 days') AND UnitId == ?", [global_unit_code])

    students = cursor.fetchall() 



     
    if flask.request.method == "GET":      
        
        return flask.render_template('home.html', students=students)
    

    if flask.request.method == "POST":
        
        print("in /home/ post")
        connect = sqlite3.connect("app\\Attendance.db")
        name = flask.request.form['studentSignIn']
        print(name)

        cursor = connect.cursor() 
        cursor.execute("INSERT INTO attendance (AttendanceID, UnitId, StudentId, Surname, Title, PreferedName, PeriodOfDay) VALUES (?,?,?,?,?,?,?)", (name,global_unit_code,2,name,2,2,2)) 
        connect.commit()

        cursor.execute("SELECT * FROM attendance WHERE DateTime > datetime('now','-1 day') AND UnitId == ?", [global_unit_code])

        students = cursor.fetchall() 
        

        return flask.render_template('home.html', students=students)





	
# CONFIGURATION - /session/ /admin/
@app.route('/session', methods=['GET', 'POST'])
def session():

    global global_unit_code
    form = SessionForm()
    if form.validate_on_submit():
        
        # Handle form submission
        session_name        = form.session_name.data
        global_unit_code    = form.unit_code.data
        unit_code           = form.unit_code.data
        
        current_year = datetime.now().year

        # Determine the semester based on the current month
        current_month = datetime.now().month
        semester = "SEM1" if current_month <= 5 else "SEM2"

        # Create Database
        database_name = f"{unit_code}_{semester}_{current_year}"

        # Printing for debugging
        print(f"Session Name: {session_name}")
        print(f"Unit Code: {unit_code}")
        print(f"Semester: {semester}")
        print(f"Database Name: {database_name}")

        # Redirect back to home page when done
        return flask.redirect(flask.url_for('home'))

    return flask.render_template('session.html', form=form)







@app.route('/admin', methods=['GET'])
def admin():
    return flask.render_template('admin.html')

# STUDENT - /student/
@app.route('/student', methods=['GET'])
def student():
    return flask.render_template('student.html')








	
# LOGIN - /login/ 
@app.route('/login', methods=['GET', 'POST'])
def login():

    
    form = LoginForm()

    if flask.request.method == 'POST' and form.validate_on_submit() :
        
        data = flask.request.form

        username = data["username"]
        password = data["password"]

        
        # SQLITE functionality
        connect = sqlite3.connect("app\\Attendance.db")
        cursor = connect.cursor() 
        cursor.execute("SELECT UserId, hash, Username FROM login WHERE ? == hash AND ? == Username", [password, username])

        # Fetch a velu that matches password (can only be one)
        students = cursor.fetchall()
        if len(students) == 0:
            print("Wrong password")
        else:
            
            
            print(students[0][0], " has logged in")
            return(flask.redirect(flask.url_for('session')))

        
            

    return flask.render_template('login.html', form=form)

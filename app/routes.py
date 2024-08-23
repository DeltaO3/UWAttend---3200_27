import flask
from app import app




# HOME -   /home/
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
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
    return flask.render_template('home.html', students=students)
	
# CONFIGURATION - /session/ /admin/
@app.route('/session', methods=['GET'])
def session():
    return flask.render_template('session.html')

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
@app.route('/login', methods=['GET'])
def login():
    return flask.render_template('login.html')

@app.route('/save_changes', methods=['POST'])
def save_changes():
    # Access form data 
    grade = request.form.get('grade')
    comment = request.form.get('comment')
    photo = request.form.get('photo')

    # Process form data here (save changes to db)

    return flask.redirect('home') 


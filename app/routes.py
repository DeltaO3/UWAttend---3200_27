import flask
from app import app
from app.forms import LoginForm



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
    return flask.render_template('student.html')
	
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

@app.route('/nfc', methods=['GET'])
def nfc():
    return flask.render_template('nfc.html')
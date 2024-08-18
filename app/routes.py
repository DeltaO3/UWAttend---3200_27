import flask
from app import app




# HOME -   /home/
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return flask.render_template('home.html')
	
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
@app.route('/login', methods=['GET'])
def login():
    return flask.render_template('login.html')

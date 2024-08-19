import flask
from app import app
from app.forms import LoginForm



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
@app.route('/login', methods=['GET', 'POST'])
def login():

    # placeholder values for testing
    username = "u1"
    password = "p1"
    
    form = LoginForm()

    if flask.request.method == 'POST' and form.validate_on_submit() :
        if form.username.data == username and form.password.data == password :
            return(flask.redirect(flask.url_for('session')))

    return flask.render_template('login.html', form=form)

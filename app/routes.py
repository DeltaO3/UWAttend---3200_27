from flask import render_template
from app import app




# HOME -   /home/
@app.route('/home', methods=['GET'])
def home():
    return flask.render_template('1.html')

# CONFIGURATION - /session/ /admin/
@app.route('/session', methods=['GET'])
def session():
    return flask.render_template('1.html')

@app.route('/admin', methods=['GET'])
def admin():
    return flask.render_template('1.html')

# STUDENT - /student/
@app.route('/student', methods=['GET'])
def student():
    return flask.render_template('1.html')
	
# LOGIN - /login/ 
@app.route('/login', methods=['GET'])
def login():
    return flask.render_template('1.html')




app.run(port=5958)

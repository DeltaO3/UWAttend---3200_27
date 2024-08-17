import flask



app = flask.Flask(__name__)






# HOME -   /home/
@app.route('/home')
def home():
    return flask.render_template('1.html')


# CONFIGURATION - /session/ /admin/
@app.route('/session')
def session():
    return flask.render_template('1.html')


@app.route('/admin')
def admin():
    return flask.render_template('1.html')





# STUDENT - /student/
@app.route('/student')
def student():
    return flask.render_template('1.html')


# LOGIN - /login/ 
@app.route('/login')
def login():
    return flask.render_template('1.html')









if __name__ == "__main__":
    app.run(port=5958)

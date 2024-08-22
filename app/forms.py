from flask_wtf import FlaskForm
import flask
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
import sqlite3
from app import app
import app.routes


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class SessionForm(FlaskForm):
    
   
    connect = sqlite3.connect("app\\Attendance.db")
    cursor = connect.cursor() 
    cursor.execute("SELECT UnitName FROM session" )



    
    students = cursor.fetchall()
    students_list = []
    
    for row in students:
        
        students_list.append(row[0])

    print(students_list)


    
    
    session_name = SelectField('Session Name', choices=students_list, validators=[DataRequired()])

    unit_code = SelectField('Unit Code', choices=[('GENG200', 'GENG200'), ('CITS3007', 'CITS3007')], validators=[DataRequired()])

    submit = SubmitField('Update')

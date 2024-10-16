from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField, HiddenField, FileField, DateField, widgets, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length
from app.database import unit_exists

class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class SessionForm(FlaskForm):

    # for each select option, value is unit_id, option is unit_code (what user sees)
    unit = SelectField('Unit Code', choices=[], validators=[DataRequired()], validate_choice=False)
    session_name = SelectField('Session Name', choices=[], validators=[DataRequired()], validate_choice=False)
    session_time = SelectField('Session Time', choices=[], validators=[DataRequired()], validate_choice=False)
    session_date = DateField('Session Date', validators=[DataRequired()])  

    # set submit button text later depending on update or config new session
    submit = SubmitField('')

#straight up copied from https://wtforms.readthedocs.io/en/3.0.x/specific_problems/?highlight=listwidget#specialty-field-tricks

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

def validate_sessionoccurence(form, field):
    if not field.data:
        raise ValidationError("Select at least one occurence")


def validate_UserType(form, field):
    if not field.data:
        print("reached here")
        raise ValidationError("Select valid user type")
        

def unit_check(form, field):
    print(f"checking unit validity, {form.unitcode.data}, {form.startdate.data}")
    if unit_exists(form.unitcode.data, form.startdate.data):
       raise ValidationError("Unit and start date combo already exist in db")
     
def edit_unit_check(form, field):
    print(f"checking unit validity, {form.unitcode.data}, {form.startdate.data}")
    if unit_exists(form.unitcode.data, form.startdate.data) and form.unitcode.data != form.currentUnit.data and form.startdate.data != form.currentUnitStart.data:
       raise ValidationError("Unit and start date combo already exist in db")
    
def password_check(form, field):
    if form.password1.data != form.password2.data:
        raise ValidationError("Passwords do not match")


def date_check(form, field):
    print(f"checking date validity, {form.startdate.data}, {form.enddate.data}")
    if form.startdate.data is not None and form.enddate.data is not None :
        if form.startdate.data > form.enddate.data :
            raise ValidationError("Start date must be before end date")

    
def is_student_num(form, field):
    if len(form.studentNumber.data) != 8 and not any(c.isdigit() for c in form.studentNumber.data):
        raise ValidationError("Student number invalid")

class AddUserForm(FlaskForm):
    UserType = SelectField(
    'User Type',
    choices=[('admin', 'Administrator'), ('coordinator', 'Coordinator')],
    validators=[validate_UserType]
    )
    email       = StringField('Email:', validators=[DataRequired()])
    submit      = SubmitField('Add User')

class CreateAccountForm(FlaskForm):
    firstName   = StringField('First name:', validators=[DataRequired()])
    lastName    = StringField('Last name:', validators=[DataRequired()])
    password1 = PasswordField('Password:', validators=[DataRequired()])
    password2 = PasswordField('Confirm password:', validators=[DataRequired(), password_check])
    submit = SubmitField('Create Account')

class ResetPasswordForm(FlaskForm):
    password1 = PasswordField('New password:', validators=[DataRequired()])
    password2 = PasswordField('Confirm new password:', validators=[DataRequired(), password_check])
    submit = SubmitField('Reset Password')

class UnitForm(FlaskForm):
    unitcode = StringField('Unit Code:', validators=[DataRequired(), unit_check])
    unitname = StringField('Unit Name:', validators=[DataRequired()])
    semester = StringField('Semester:', validators=[DataRequired()])
    startdate = DateField('Start Date', validators=[DataRequired(), date_check])
    enddate = DateField('End Date', validators=[DataRequired()])
    consentcheck = BooleanField('Photo Consent Required?')
    assessmentcheck = BooleanField('Sessions Assessed?')
    commentsenabled = BooleanField('Comments Enabled?', default=True)
    sessionnames = StringField('Session Names:', render_kw={"placeholder":"Add sessions"})
    sessions = HiddenField("Sessions", validators=[DataRequired()])
    sessionoccurence = SelectField(
		'Session Occurence',
		choices=[('Morning/Afternoon','Morning/Afternoon'), ('Hours','Hours')],
		validators=[validate_sessionoccurence])
    commentsuggestions = StringField('Comment Suggestions:', render_kw={"placeholder":"Optional, add suggestions"})
    comments = HiddenField("Comments")
   

class AddUnitForm(UnitForm):
    facilitatorfile = FileField('Facilitator List CSV upload', validators=[FileRequired(), FileAllowed(['csv'], "Only accepts .csv files")],render_kw={"accept": ".csv"})
    studentfile = FileField('Student List CSV Upload:', validators=[FileRequired(), FileAllowed(['csv'], "Only accepts .csv files")],render_kw={"accept": ".csv"})
    submit = SubmitField('Add Unit')

class UpdateUnitForm(UnitForm):
    #Overwrite unit code to use a different validator
    unitcode = StringField('Unit Code:', validators=[DataRequired(), edit_unit_check]) 
    #While you can edit  if you are a malicious attacker, all it will do is make you submit even less. 
    currentUnit = HiddenField("Current Unit") 
    currentUnitStart = HiddenField("Current Start")
    submit = SubmitField('Update Unit')

class AddStudentForm(FlaskForm):
    studentNumber = StringField("Student Number:", validators=[DataRequired(), is_student_num])
    firstName = StringField("First Name:", validators=[DataRequired()])
    preferredName = StringField("Preferred Name:", validators=[DataRequired()])
    lastName = StringField("Last Name:", validators=[DataRequired()])
    title = StringField("Title:", validators=[DataRequired()])
    submit = SubmitField("Add Student")
    
class UploadStudentForm(FlaskForm):
    studentfile = FileField('Student List CSV Upload:', validators=[FileRequired(), FileAllowed(['csv'], "Only accepts .csv files")],render_kw={"accept": ".csv"})
    submit = SubmitField("Upload")

class StudentSignInForm(FlaskForm):
    student_sign_in = StringField('Sign in Student', validators=[DataRequired()])
    consent_status = HiddenField('Consent Status', default="none")
    studentID = HiddenField('Student ID')  
    session_id = HiddenField('Session ID')  

class AttendanceChangesForm(FlaskForm):
    student_id = HiddenField('Student ID')
    signInTime = StringField('Sign in time')
    signOutTime = StringField('Sign out time')
    login = BooleanField('Login')
    consent = BooleanField('Photo Consent')
    grade = StringField('Grade')
    comments = TextAreaField('Leave/edit comments')
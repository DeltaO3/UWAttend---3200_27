from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField, HiddenField, FileField, DateField, widgets
from wtforms.validators import DataRequired, ValidationError
from app.database import unit_exists

class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class SessionForm(FlaskForm):
    session_name = SelectField(
        'Session Name',
        choices=[],
        validators=[DataRequired()],
        validate_choice=False
    )

    # for each select option, value is unit_id, option is unit_code (what user sees)
    unit = SelectField(
        'Unit Code',
        choices=[],
        validators=[DataRequired()],
        validate_choice=False
    )

    session_time = SelectField(
        'Session Time',
        choices=[],
        validators=[DataRequired()],
        validate_choice=False
    )

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
        raise ValidationError("Select at least one occurence")
        

def unit_check(form, field):
    print(f"checking unit validity, {form.unitcode.data}, {form.startdate.data}")
    if unit_exists(form.unitcode.data, form.startdate.data):
       raise ValidationError("Unit and start date combo already exist in db")
     
def date_check(form, field):
	print(f"checking date validity, {form.startdate.data}, {form.enddate.data}")
	if form.startdate.data > form.enddate.data:
		raise ValidationError("Start date must be before end date")

class AddUserForm(FlaskForm):
    
    UserType = SelectField(
    'User Type',
    choices=[('admin', 'Administrator'), ('coordinator', 'Coordinator'), ('facilitator', 'Facilitator')],
    validators=[validate_UserType]
    )
    email       = StringField('Email:', validators=[DataRequired()])
    firstName   = StringField('First name:', validators=[DataRequired()])
    lastName    = StringField('Last name:', validators=[DataRequired()])
    passwordHash = StringField('Password:', validators=[DataRequired()])
    submit      = SubmitField('Add User')
    
class AddUnitForm(FlaskForm):
    unitcode = StringField('Unit Code:', validators=[DataRequired(), unit_check])
    unitname = StringField('Unit Name:', validators=[DataRequired()])
    semester = StringField('Semester:', validators=[DataRequired()])
    startdate = DateField('Start Date', validators=[DataRequired(), date_check])
    enddate = DateField('End Date', validators=[DataRequired()])
	#Need to add custom validators to check if files uploaded end in csv
    sessionnames = StringField('Session Names:', validators=[DataRequired()], render_kw={"placeholder":"separate with |"})
    facilitatorfile = FileField('Facilitator IDs', validators=[FileRequired(), FileAllowed(['csv'], "Only accepts .csv files")])
    studentfile = FileField('Student List CSV Upload:', validators=[FileRequired(), FileAllowed(['csv'], "Only accepts .csv files")])
    consentcheck = BooleanField('Photo Consent Required?')
    sessionoccurence = MultiCheckboxField(
		'Session Occurence',
		choices=[('Morning','Morning'), ('Afternoon', 'Afternoon')
		],
		validators=[validate_sessionoccurence])
    assessmentcheck = BooleanField('Sessions Assessed?')
    commentsenabled = BooleanField('Student Comments Enabled?')
    commentsuggestions = StringField('Comment Suggestions:', render_kw={"placeholder":"Optional; separate with |"})
    submit = SubmitField('Add Unit')
    
class StudentSignInForm(FlaskForm):
    student_sign_in = StringField('Sign in Student', validators=[DataRequired()])
    consent_status = HiddenField('Consent Status', default="none")
    studentID = HiddenField('Student ID')  
    sessionID = StringField('Session ID')  

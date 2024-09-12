from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, HiddenField, FileField
from wtforms.validators import DataRequired, ValidationError

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

    submit = SubmitField('Update')

class AddUnitForm(FlaskForm):
    unitcode = StringField('Unit Code:', validators=[DataRequired()])
    semester = StringField('Semester:', validators=[DataRequired()])
    #Need to add custom validators to check if files uploaded end in csv
    studentfile = FileField('Student List CSV Upload:', validators=[DataRequired()])
    facilitatorfile = FileField('Facilitator List CSV Upload:')
    consentcheck = BooleanField('Photo Consent Required?')
    sessionnames = StringField('Session Names:', validators=[DataRequired()])
    sessionoccurence = SelectField(
        'Session Occurence',
        choices=[('Morning','Morning'), ('Afternoon', 'Afternoon')
        ])
    assessmentcheck = BooleanField('Sessions Assessed?')
    commentsenabled = BooleanField('Student Comments Enabled?')
    commentsuggestions = StringField('Comment Suggestions:')
    submit = SubmitField('Add Unit')
    
class StudentSignInForm(FlaskForm):
    student_sign_in = StringField('Sign in Student', validators=[DataRequired()])
    consent_status = HiddenField('Consent Status', default="none")

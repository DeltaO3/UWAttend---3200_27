from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField, HiddenField, FileField, DateField, widgets
from wtforms.validators import DataRequired, ValidationError

class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class SessionForm(FlaskForm):
    session_name = SelectField(
        'Session Name',
        choices=[
            ('Safety', 'Safety'), ('CAD', 'CAD'), ('Computer', 'Computer'),
            ('PipeWorks', 'PipeWorks'), ('Measurement', 'Measurement'),
            ('ReverseEng', 'Reverse Engineering'), ('DataMapping', 'Data Mapping'),
            ('Soldering', 'Soldering'), ('HandTools', 'Hand Tools')
        ],
        validators=[DataRequired()]
    )

    unit_code = SelectField(
        'Unit Code',
        choices=[
            ('GENG200', 'GENG200'), ('CITS3007', 'CITS3007')
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField('Update')

#straight up copied from https://wtforms.readthedocs.io/en/3.0.x/specific_problems/?highlight=listwidget#specialty-field-tricks

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

def validate_sessionoccurence(form, field):
    if not field.data:
        print("reached here")
        raise ValidationError("Select at least one occurence")
        
    
class AddUnitForm(FlaskForm):
    unitcode = StringField('Unit Code:', validators=[DataRequired()])
    semester = StringField('Semester:', validators=[DataRequired()])
    startdate = DateField('Start Date', validators=[DataRequired()])
    enddate = DateField('End Date', validators=[DataRequired()])
    #Need to add custom validators to check if files uploaded end in csv
    facilitatorlist = StringField('Facilitator IDs', validators=[DataRequired()], render_kw={"placeholder":"separate with |"})
    studentfile = FileField('Student List CSV Upload:', validators=[DataRequired()])
    consentcheck = BooleanField('Photo Consent Required?')
    sessionnames = StringField('Session Names:', validators=[DataRequired()], render_kw={"placeholder":"separate with |"})
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
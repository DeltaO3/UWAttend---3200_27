from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
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

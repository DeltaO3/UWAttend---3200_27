import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, Unit, Student, Session, Attendance

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Unit': Unit, 'Student': Student, 'Session': Session, 'Attendance': Attendance}
import datetime
from app import app, db
from app.database import *
from .emails import *
from .utilites import generate_temp_password

with app.app_context():
	print("Adding Adrian as an admin user")
	AddUser("adrian.keating@uwa.edu.au", "Adrian", "Keating", generate_temp_password(), "admin")
	send_email_ses("noreply@uwaengineeringprojects.com", "adrian.keating@uwa.edu.au", 'welcome')
	print("Emailed Adrian a link to create his account")
	

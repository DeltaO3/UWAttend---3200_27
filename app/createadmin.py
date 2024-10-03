from dotenv import load_dotenv
from flask import Flask
from config import Config
import os
from app import app, db
from app.database import AddUser, GetUser

load_dotenv(override=True)

email=os.getenv("EMAIL")
firstname=os.getenv("FIRSTNAME")
lastname=os.getenv("LASTNAME")
password=os.getenv("PASSWORD")
usertype=os.getenv("USERTYPE")

#uses email as that is unique.
with app.app_context():
	if(not GetUser(email=email)):
		print("adding admin to database")
		AddUser(email, firstname, lastname, password, usertype)
		admin = GetUser(email=email)
		# print(f"{admin.firstName} {admin.lastName} {admin.userID} is now in database")
	else:
		print("user already in database")
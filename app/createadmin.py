from dotenv import load_dotenv
from flask import Flask
from config import Config
import os
from app import app, db
from app.database import AddUser, GetUser

load_dotenv(override=True)

uwaID=os.getenv("UWAID")
firstname=os.getenv("FIRSTNAME")
lastname=os.getenv("LASTNAME")
password=os.getenv("PASSWORD")
usertype=os.getenv("USERTYPE")

#uses uwaID as that is unique.
with app.app_context():
	if(not GetUser(uwaID=uwaID)):
		print("adding admin to database")
		AddUser(uwaID, firstname, lastname, password, usertype)
		admin = GetUser(uwaID=uwaID)
		# print(f"{admin.firstName} {admin.lastName} {admin.userID} is now in database")
	else:
		print("user already in database")
from dotenv import load_dotenv
from flask import Flask
from config import Config
import os
from app import app, db
from app.database import AddUser, GetUser

load_dotenv()

id=os.getenv("ID")
uwaID=os.getenv("UWAID")
firstname=os.getenv("FIRSTNAME")
lastname=os.getenv("LASTNAME")
password=os.getenv("PASSWORD")
type=os.getenv("USERTYPE")

with app.app_context():
	if(not GetUser(userID=id)):
		print("adding admin to database")
		AddUser(id, uwaID, firstname, lastname, password, type)
		admin = GetUser(userID=id)
		print(f"{admin[0].firstName} {admin[0].lastName} is now in database")
	else:
		print("user already in database")
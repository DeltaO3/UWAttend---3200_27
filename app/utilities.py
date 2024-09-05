# Utilities file for storing miscellaneous functions that dont neatly fit into other categories
# (i.e. not models, databases, etc)

import csv
import os
import zipfile
from io import StringIO
from app import app, db
from app.models import Student, User, Attendance, Session, Unit
from app.database import AddStudent
from app.helpers import get_perth_time

# Set of functions used to read and populate students into the database from a csv file.
# Checklist for future
# 1. DONE Connect to actual database for population
# 2. TODO Create upload button for frontend that uses these functions
# 3. TODO Remove "if __name__ == "__main__:" and instead incorporate code into Flask

# PLACEHOLDER FUNCTION: This will be replaced with import button on frontend
# Reads a CSV file and returns a list of dictionaries where each dictionary represents a row.
def read_csv_file(file_path):
    data = []
    if os.path.exists(file_path):
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    else:
        print(f"The file {file_path} does not exist.")
    return data

# Checks for duplicate students
def student_exists(student_number):
    return db.session.query(Student).filter_by(studentNumber=student_number).first() is not None

# Imports students into the database given a .csv file
def import_student_in_db(data):
    for record in data:
        # PLACEHOLDER: Do we need unitID for students???
        unit = 'CITS3000'

        student_number = record['Person ID']
        if student_exists(student_number):
            print(f"Duplicate found: {record['Given Names']} {record['Surname']} (ID: {student_number}) - Skipping import.")
            continue

        # Call the AddStudent function from database.py
        AddStudent(
            studentID=None,  # Assuming None so the database auto-generates this
            studentNumber=record['Person ID'],
            firstName=record['Given Names'],
            lastName=record['Surname'],
            title=record['Title'],
            preferredName=record['Preferred Given Name'],
            unitID=unit,  # Assuming a default unit ID, replace as needed
            consent=0  # Setting consent to 0 as per your requirements
        )
        print(f"Added student: {record['Given Names']} {record['Surname']} (ID: {student_number})")

# Process a .csv file by reading and then importing into "student" table.
def process_csv(file_path):
    with app.app_context():
        # Read the data from the CSV file
        data = read_csv_file(file_path)
        if data:
            # Import the data to the database
            import_student_in_db(data)

# Export a single table's data to a CSV format and return it as a string
def export_table_to_csv(model):
    # Query all records from the model's table
    records = db.session.query(model).all()

    if records:
        # Get the column names from the model's attributes
        columns = records[0].__table__.columns.keys()

        # Use StringIO to write CSV data in-memory
        csvfile = StringIO()
        writer = csv.writer(csvfile)
        writer.writerow(columns)  # Write the header

        # Write each record as a row in the CSV
        for record in records:
            writer.writerow([getattr(record, col) for col in columns])

        return csvfile.getvalue()
    else:
        print(f"No data found for {model.__tablename__}")
        return None

# Export all tables to a single ZIP file containing multiple CSV files
def export_all_to_zip(zip_filename):
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:

        # Export the Student table
        student_csv = export_table_to_csv(Student)
        if student_csv:
            zipf.writestr('students.csv', student_csv)
            print("Exported students.csv")

        # Export the User table
        user_csv = export_table_to_csv(User)
        if user_csv:
            zipf.writestr('users.csv', user_csv)
            print("Exported users.csv")

        # Export the Attendance table
        attendance_csv = export_table_to_csv(Attendance)
        if attendance_csv:
            zipf.writestr('attendance.csv', attendance_csv)
            print("Exported attendance.csv")

        # Export the Session table
        session_csv = export_table_to_csv(Session)
        if session_csv:
            zipf.writestr('sessions.csv', session_csv)
            print("Exported sessions.csv")

        # Export the Unit table
        unit_csv = export_table_to_csv(Unit)
        if unit_csv:
            zipf.writestr('units.csv', unit_csv)
            print("Exported units.csv")

    print(f"All tables have been exported to {zip_filename}")

# For testing purposes. Remove when integrating into main application
if __name__ == "__main__":
    csv_file_path = 'test.csv'

    # Process the CSV file
    process_csv(csv_file_path)

    with app.app_context():
        # Export CSV File
        export_all_to_zip("database.zip")

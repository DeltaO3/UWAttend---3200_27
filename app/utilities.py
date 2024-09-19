# Utilities file for storing miscellaneous functions that dont neatly fit into other categories
# (i.e. not models, databases, etc)

import csv
import os
import zipfile
from io import StringIO
from app import app, db
from app.models import Student, User, Attendance, Session, Unit
from app.database import AddStudent, GetStudent, GetAttendance, GetSessionForExport, GetAllUsers, GetUnit, student_exists

# Set of functions used to read and populate students into the database from a csv file.
# Checklist for future
# 1. DONE Connect to actual database for population
# 2. DONE Create upload button for frontend that uses these functions
# 3. DONE Remove "if __name__ == "__main__:" and instead incorporate code into Flask

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

# Imports students into the database given a .csv file
def import_student_in_db(data, unit_id):
    for record in data:

        student_number = record['Person ID']
        if student_exists(student_number, unit_id):
            print(f"Duplicate found: {record['Given Names']} {record['Surname']} (ID: {student_number}) - Skipping import.")
            continue

        # Call the AddStudent function from database.py
        AddStudent(
            studentNumber=record['Person ID'],
            firstName=record['Given Names'],
            lastName=record['Surname'],
            title=record['Title'],
            preferredName=record['Preferred Given Name'],
            unitID=unit_id,  # Assuming a default unit ID, replace as needed
            consent=0  # Setting consent to 0 as per your requirements
        )
        print(f"Added student: {record['Given Names']} {record['Surname']} (ID: {student_number})")

# Process a .csv file by reading and then importing into "student" table.
def process_csv(file_path, unit_id):
    with app.app_context():
        # Read the data from the CSV file
        data = read_csv_file(file_path)
        if data:
            # Import the data to the database
            import_student_in_db(data, unit_id)

# Export a single table's data to a CSV format and return it as a string
def export_table_to_csv(fetch_function):
    # Query all records from the model's table
    records = fetch_function()

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
        print(f"No data found for {fetch_function}")
        return None

# Creates attendancerecord.csv for exporting
def export_attendance_records_csv():
    # Perform a query that joins the necessary tables
    records = db.session.query(
        Attendance,
        Student,
        Session,
        Unit
    ).join(
        Student, Attendance.studentID == Student.studentID
    ).join(
        Session, Attendance.sessionID == Session.sessionID
    ).join(
        Unit, Student.unitID == Unit.unitID
    ).all()

    if records:
        # Define the headers
        columns = [
            'studentNumber', 'firstName', 'lastName', 'title', 'preferredName', 'unitCode',
            'sessionDate', 'sessionName', 'sessionTime', 'signInTime', 'signOutTime',
            'marks', 'comments', 'consent'
        ]

        csvfile = StringIO()
        writer = csv.writer(csvfile)
        writer.writerow(columns)  # Write the header

        # Iterate over each record and write to csvfile
        for attendance, student, session, unit in records:
            row = [
                student.studentNumber,
                student.firstName,
                student.lastName,
                student.title,
                student.preferredName,
                unit.unitCode,
                session.sessionDate.strftime('%Y-%m-%d') if session.sessionDate else '',
                session.sessionName,
                session.sessionTime,
                attendance.signInTime.strftime('%H:%M:%S') if attendance.signInTime else '',
                attendance.signOutTime.strftime('%H:%M:%S') if attendance.signOutTime else '',
                attendance.marks if attendance.marks else '', # Marks, blank if none
                attendance.comments if attendance.comments else '', # Comments, blank if none
                'Yes' if attendance.consent_given else 'No' # Consent status ('Yes' or 'No')
            ]
            writer.writerow(row)
        return csvfile.getvalue()
    else:
        print("No attendance records found")
        return None

# Export all tables to a single ZIP file containing multiple CSV files
def export_all_to_zip(zip_filename):
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:

        # Export the Student table
        student_csv = export_table_to_csv(GetStudent)
        if student_csv:
            zipf.writestr('students.csv', student_csv)
            print("Exported students.csv")

        # Export the User table
        user_csv = export_table_to_csv(GetAllUsers)
        if user_csv:
            zipf.writestr('users.csv', user_csv)
            print("Exported users.csv")

        # Export the Attendance table
        attendance_csv = export_table_to_csv(GetAttendance)
        if attendance_csv:
            zipf.writestr('attendance.csv', attendance_csv)
            print("Exported attendance.csv")

        # Export the Session table
        session_csv = export_table_to_csv(GetSessionForExport)
        if session_csv:
            zipf.writestr('sessions.csv', session_csv)
            print("Exported sessions.csv")

        # Export the Unit table
        unit_csv = export_table_to_csv(GetUnit)
        if unit_csv:
            zipf.writestr('units.csv', unit_csv)
            print("Exported units.csv")

        # Export the Attendance Records CSV
        attendance_records_csv = export_attendance_records_csv()
        if attendance_records_csv:
            zipf.writestr('attendancerecord.csv', attendance_records_csv)
            print("Exported attendancerecord.csv")

    print(f"All tables have been exported to {zip_filename}")

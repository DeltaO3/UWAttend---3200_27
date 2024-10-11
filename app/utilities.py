# Utilities file for storing miscellaneous functions that dont neatly fit into other categories
# (i.e. not models, databases, etc)

import csv
import os
import zipfile
from io import StringIO
from app import app, db
from app.models import Student, User, Attendance, Session, Unit
from app.database import AddStudent, GetStudent, GetAttendance, GetSessionForExport, GetAllUsers, GetUnit, student_exists, GetUser, AddUser, AddUnitToFacilitator

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

    unit = GetUnit(unitID=unit_id)

    if not unit:
        print("Student cannot be added to unit until unit is initialised")
        return
    
    unit = unit[0]

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
            consent='no' if unit.consent else 'not required' # Setting consent to no as per your requirements
        )
        print(f"Added student: {record['Given Names']} {record['Surname']} (ID: {student_number})")

def import_facilitator_in_db(data, unit_id, current_user):

    for record in data:
        facilitator = record['Facilitator Email']
        #Add facilitator as user if not in DB
        if(not GetUser(email=facilitator)):
            print(f"Adding new user: {facilitator}")
            AddUser(facilitator, "placeholder", "placeholder", facilitator, "facilitator")
        #add this unit to facilator
        if(facilitator == current_user.email):
            print(f"skipping user {facilitator} as it is the currently logged in user.")
            continue
        print(f"Adding unit {unit_id} to facilitator {facilitator}")
        AddUnitToFacilitator(facilitator, unit_id)

# Process a .csv file by reading and then importing into "student" table. 
# If current user is passsed, processes file as a facilitator file
def process_csvs(student_file_path, facilitator_file_path):
    with app.app_context():
        # Read the data from the CSV file
        s_data = read_csv_file(student_file_path)
        f_data = read_csv_file(facilitator_file_path)
        if s_data and f_data:
            # Import the data to the database
            #Ensure passed csv file is correct type 
            errors = []
            if len(s_data[0]) != 5:
                print("Not a student csv!")
                errors.append("Student csv format is incorrect")
            if len(f_data[0]) != 1:
                print("Not a facilitator csv!")
                errors.append("Facilitator csv format is incorrect")
            if errors:
                msg = errors[0] if len(errors) == 1 else errors[0] + ", " + errors[1]
                return 0, 0, msg
            return s_data, f_data, 0 #return value for routes validation

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
                attendance.consent_given # Consent give: yes, no or not required (if unit is configured to not ask consent)
            ]
            writer.writerow(row)
        return csvfile.getvalue()
    else:
        print("No attendance records found")
        return None

def export_attendance_records_columns():
    # Query the attendance records joined with students, sessions, and units
    records = db.session.query(
        Attendance,
        Student,
        Session,
        Unit,
        User
    ).join(
        Student, Attendance.studentID == Student.studentID
    ).join(
        Session, Attendance.sessionID == Session.sessionID
    ).join(
        Unit, Student.unitID == Unit.unitID
    ).join(
        User, Attendance.facilitatorID == User.userID
    ).all()

    if records:
        # Initialize a dictionary to store students, keyed by (studentNumber, unitCode) for uniqueness per unit
        attendance_data = {}

        # Iterate over the records and organize by unique student-unit combinations
        for attendance, student, session, unit, facilitator in records:
            # Use a tuple (studentNumber, unitCode) as the key to ensure uniqueness per unit
            unique_key = (student.studentNumber, unit.unitCode)
            if unique_key not in attendance_data:
                attendance_data[unique_key] = {
                    'studentNumber': student.studentNumber,
                    'firstName': student.firstName,
                    'lastName': student.lastName,
                    'title': student.title,
                    'preferredName': student.preferredName,
                    'unitCode': unit.unitCode,
                    'consent': 'Yes' if attendance.consent_given else 'No',
                }

            # Format session data for attendance: [sessionName][FacilitatorName]signInTime;signOutTime
            session_key = f"{session.sessionDate.strftime('%Y_%B_%d')}_{session.sessionTime}"
            sign_in_time = (
                attendance.signInTime.strftime('%H:%M:%S')
                if attendance.signInTime
                else ''
            )
            sign_out_time = (
                attendance.signOutTime.strftime('%H:%M:%S')
                if attendance.signOutTime
                else ''
            )
            facilitator_name = f"{facilitator.firstName} {facilitator.lastName}"
            attendance_info = f"[{session.sessionName}][{facilitator_name}]{sign_in_time};{sign_out_time}"

            # Store attendance_info under session_key
            attendance_data[unique_key][session_key] = attendance_info

            # Format grade data according to your specified rules
            marks = attendance.marks if attendance.marks else ''
            comments = attendance.comments if attendance.comments else ''

            if marks and comments:
                grade_info = f"{marks};comment={comments}"
            elif marks:
                grade_info = f"{marks};"
            elif comments:
                grade_info = f";comment={comments}"
            else:
                grade_info = ''

            # Store grade_info under session_key + '_Grade'
            attendance_data[unique_key][f"{session_key}_Grade"] = grade_info

        # Prepare the headers
        headers = [
            'studentNumber', 'firstName', 'lastName', 'title', 'preferredName', 'unitCode', 'consent'
        ]

        # Collect all session_keys
        session_keys = set()
        for student_record in attendance_data.values():
            for key in student_record:
                if key not in headers:
                    if key.endswith('_Grade'):
                        session_keys.add(key[:-6])  # Remove '_Grade' from key
                    else:
                        session_keys.add(key)

        # Sort the session_keys and build headers
        sorted_session_keys = sorted(session_keys)

        for session_key in sorted_session_keys:
            headers.append(session_key)
            headers.append(f"{session_key}_Grade")

        # Create a list of rows (each row represents a unique student-unit combination)
        rows = []
        for student_unit_key, student_record in attendance_data.items():
            # Print the student record before creating the row
            row = [student_record.get(header, '') for header in headers]
            rows.append(row)

        # Convert to CSV with proper quoting
        csvfile = StringIO()
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(headers)  # Write the header
        writer.writerows(rows)    # Write all student rows

        return csvfile.getvalue()

    else:
        print("No attendance records found.")
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

        # Export the Attendance Records CSV
        attendance_records_columns = export_attendance_records_columns()
        if attendance_records_columns:
            zipf.writestr('attendancerecordCOLUMNS.csv', attendance_records_columns)
            print("Exported attendancerecordCOLUMNS.csv")

    print(f"All tables have been exported to {zip_filename}")

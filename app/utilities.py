# Utilities file for storing miscellaneous functions that dont neatly fit into other categories
# (i.e. not models, databases, etc)

import csv
import os
import zipfile
import string 
import secrets
from io import StringIO
from app import app, db
from .models import *
from .database import *
from .emails import *
import pandas as pd

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

        student_number = record['Student ID']
        if student_exists(student_number, unit_id):
            print(f"Duplicate found: {record['Given Names']} {record['Surname']} (ID: {student_number}) - Skipping import.")
            continue

        # Call the AddStudent function from database.py
        AddStudent(
            studentNumber=record['Student ID'],
            firstName=record['Given Names'],
            lastName=record['Surname'],
            title=record['Title'],
            preferredName=record['Preferred Name'],
            unitID=unit_id,  # Assuming a default unit ID, replace as needed
            consent='no' if unit.consent else 'not required' # Setting consent to no as per your requirements
        )
        print(f"Added student: {record['Given Names']} {record['Surname']} (ID: {student_number})")

def import_facilitator_in_db(data, unit_id, current_user):

    for record in data:        
        facilitator = record['Facilitator Email']
        
        #Add facilitator as user if not in DB
        if(not GetUser(email=facilitator)):
            temp_password = generate_temp_password()
            print(f"Adding new user: {facilitator}")
            AddUser(facilitator, "placeholder", "placeholder", temp_password, "facilitator")
            send_email_ses("noreply@uwaengineeringprojects.com", facilitator, 'welcome')
        # add this unit to facilator
        if(facilitator == current_user.email):
            print(f"skipping user {facilitator} as it is the currently logged in user.")
            continue
        print(f"Adding unit {unit_id} to facilitator {facilitator}")
        AddUnitToFacilitator(facilitator, unit_id)

def generate_temp_password(length=12):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

# Process a .csv file by reading and then importing into "student" table. 
# If current user is passsed, processes file as a facilitator file
def process_csvs(student_file_path, facilitator_file_path):
    with app.app_context():
        # Read the data from the CSV file
        s_data = read_csv_file(student_file_path)
        if facilitator_file_path is not None:
            f_data = read_csv_file(facilitator_file_path)
        else:
            f_data = False
        if s_data and f_data:
            # Import the data to the database
            #Ensure passed csv file is correct type 
            errors = validate_csv_headers(s_data[0], f_data[0])

            if errors:
                msg = ''
                for error in errors :
                    msg += error + ', '
                return 0, 0, msg[:-2]
            return s_data, f_data, 0 #return value for routes validation
        if s_data and facilitator_file_path is None:
            if len(s_data[0]) != 5:
                print("Not a student csv!")
                return 0, "Student csv format is incorrect"
            else:
                return s_data, 0

# checks if headers are correct based on first row only
def validate_csv_headers(s_data_row, f_data_row) :

    errors = []

    if len(s_data_row) != 5:
        print("Not a student csv!")
        errors.append("Student csv format is incorrect")
    if len(f_data_row) != 1:
        print("Not a facilitator csv!")
        errors.append("Facilitator csv format is incorrect")

    student_headers = ["Student ID", "Surname", "Title", "Given Names", "Preferred Name"]
    factilitator_headers = ["Facilitator Email"]

    for header in student_headers :
        if header not in s_data_row :
            errors.append(f"{header} header not detected in student csv")

    for header in factilitator_headers :
        if header not in f_data_row :
            errors.append(f"{header} header not detected in facilitator csv")

    return errors


# Export a single table's data to a CSV format and return it as a string
def export_table_to_csv(fetch_function, current_user_id, current_user_type):
# Get accessible unit IDs if the user is not an admin
    unit_ids = GetAccessibleUnitIDs(current_user_id)

    # Query all records from the model's table
    query = fetch_function()

    # Filter based on unit ID if not admin
    if unit_ids and hasattr(query[0], "unitID"):
        query = [record for record in query if record.unitID in unit_ids]

    # Additional filtering for the Attendance table
    if fetch_function == GetAttendance:
        # Filter attendance records based on session's unit ID
        session_unit_mapping = {
            session.sessionID: session.unitID for session in db.session.query(Session).all()
        }
        # Filter attendance where the session's unitID is in the list of accessible unit IDs
        query = [
            record for record in query
            if session_unit_mapping.get(record.sessionID) in unit_ids
        ]

    if query:
        # Get the column names from the model's attributes
        columns = query[0].__table__.columns.keys()

        # If exporting the User table, exclude the passwordHash column
        if fetch_function == GetAllUsers:
            columns = [col for col in columns if col not in ['passwordHash', 'token']]

        # Use StringIO to write CSV data in-memory
        csvfile = StringIO()
        writer = csv.writer(csvfile)
        writer.writerow(columns)  # Write the header

        # Write each record as a row in the CSV
        for record in query:
            writer.writerow([getattr(record, col) for col in columns])

        return csvfile.getvalue()
    else:
        print(f"No data found for {fetch_function}")
        return None

# Creates attendancerecord.csv for exporting
def export_attendance_records_csv(current_user_id, current_user_type):

    unit_ids = GetAccessibleUnitIDs(current_user_id)
    if not unit_ids:
        print("No units found for the current coordinator")
        return None

    # Perform a query that joins the necessary tables
    query = db.session.query(
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
    )

    if unit_ids:
            query = query.filter(Unit.unitID.in_(unit_ids))

    records = query.all()

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

def export_attendance_records_columns(current_user_id, current_user_type):

    unit_ids = GetAccessibleUnitIDs(current_user_id)
    if not unit_ids:
        print("No units found for the current coordinator")
        return None

    # Query the attendance records joined with students, sessions, and units
    query = db.session.query(
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
    )

    if unit_ids:
        query = query.filter(Unit.unitID.in_(unit_ids))

    records = query.all()

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
                    'unitCode': unit.unitCode
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
            consent_status = "yes" if attendance.consent_given == "yes" else "no"
            attendance_info = f"[{session.sessionName}][{facilitator_name}]{sign_in_time};{sign_out_time};consent_given={consent_status}"

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
            'studentNumber', 'firstName', 'lastName', 'title', 'preferredName', 'unitCode'
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
def export_all_to_zip(zip_filename, current_user_id, current_user_type):
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:

        # Export the Student table
        student_csv = export_table_to_csv(GetStudent, current_user_id, current_user_type)
        if student_csv:
            zipf.writestr('students.csv', student_csv)
            print("Exported students.csv")

        # Export the User table only if the user is an admin
        user_csv = None
        if current_user_type == "admin":
            user_csv = export_table_to_csv(GetAllUsers, current_user_id, current_user_type)
            if user_csv:
                zipf.writestr('users.csv', user_csv)
                print("Exported users.csv")

        # Export the Attendance table
        attendance_csv = export_table_to_csv(GetAttendance, current_user_id, current_user_type)
        if attendance_csv:
            zipf.writestr('attendance.csv', attendance_csv)
            print("Exported attendance.csv")

        # Export the Session table
        session_csv = export_table_to_csv(GetSessionForExport, current_user_id, current_user_type)
        if session_csv:
            zipf.writestr('sessions.csv', session_csv)
            print("Exported sessions.csv")

        # Export the Unit table
        unit_csv = export_table_to_csv(GetUnit, current_user_id, current_user_type)
        if unit_csv:
            zipf.writestr('units.csv', unit_csv)
            print("Exported units.csv")

        # Export the Attendance Records CSV
        attendance_records_csv = export_attendance_records_csv(current_user_id, current_user_type)
        if attendance_records_csv:
            zipf.writestr('attendancerecord.csv', attendance_records_csv)
            print("Exported attendancerecord.csv")

        # Export the Attendance Records CSV
        attendance_records_columns = export_attendance_records_columns(current_user_id, current_user_type)
        if attendance_records_columns:
            zipf.writestr('attendancerecordCOLUMNS.csv', attendance_records_columns)
            print("Exported attendancerecordCOLUMNS.csv")

    print(f"All tables have been exported to {zip_filename}")

# Function to filter CSV files by unitCode
def filter_exported_csv_by_unit(zip_filename, unit_code):
    print(f"Filtering exported CSVs by unitCode: {unit_code}")

    # Get the unit ID from the unitCode
    unit_id = get_unit_id_by_code(unit_code)

    if not unit_id:
        print(f"No unit found for unitCode: {unit_code}")
        return zip_filename

    # Create a new ZIP file to store filtered CSVs
    filtered_zip_filename = "filtered_" + zip_filename
    with zipfile.ZipFile(zip_filename, 'r') as z, zipfile.ZipFile(filtered_zip_filename, 'w', zipfile.ZIP_DEFLATED) as filtered_zip:
        # First load session.csv to map sessionID to unitID
        session_data = None
        if 'sessions.csv' in z.namelist():
            with z.open('sessions.csv') as f:
                session_data = pd.read_csv(f)
                session_data = session_data[['sessionID', 'unitID']]  # Keep only sessionID and unitID columns

        # Iterate over each file in the original zip
        for file in z.namelist():
            with z.open(file) as f:
                df = pd.read_csv(f)

                if 'unitCode' in df.columns:
                    # Directly filter by unitCode
                    df_filtered = df[df['unitCode'] == unit_code]
                elif 'unitID' in df.columns:
                    # Filter by unitID
                    df_filtered = df[df['unitID'] == unit_id]
                elif file == 'attendance.csv' and session_data is not None:
                    # Filter attendance.csv by session's unitID
                    if 'sessionID' in df.columns:
                        # Merge attendance data with session data to get the unitID for each session
                        df = df.merge(session_data, on='sessionID', how='left')
                        df_filtered = df[df['unitID'] == unit_id]
                    else:
                        df_filtered = df  # If no sessionID column, leave unfiltered
                else:
                    # If no filtering is needed for this file, keep it as-is
                    df_filtered = df

                # Write the filtered DataFrame back to the new zip
                csv_buffer = StringIO()
                df_filtered.to_csv(csv_buffer, index=False)
                filtered_zip.writestr(file, csv_buffer.getvalue())

    print(f"Filtered CSVs by unitCode: {unit_code}, saved as {filtered_zip_filename}")
    return filtered_zip_filename

# Helper function to get the unitID from a unitCode
def get_unit_id_by_code(unit_code):
    unit = db.session.query(Unit).filter_by(unitCode=unit_code).first()
    if unit:
        return unit.unitID
    return None

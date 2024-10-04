from datetime import datetime
import pytz
from flask_login import current_user

sessionTimeDefinitions = {
    "Morning" : (datetime.strptime('7:45', '%H:%M').time(), datetime.strptime('13:00', '%H:%M').time()),
    "Afternoon" : (datetime.strptime('13:01', '%H:%M').time(), datetime.strptime('18:30', '%H:%M').time()),
    "8am" : (datetime.strptime('7:45', '%H:%M').time(), datetime.strptime('8:15', '%H:%M').time()),
    "9am" : (datetime.strptime('8:45', '%H:%M').time(), datetime.strptime('9:15', '%H:%M').time()),
    "10am" : (datetime.strptime('9:45', '%H:%M').time(), datetime.strptime('10:15', '%H:%M').time()),
    "11am" : (datetime.strptime('10:45', '%H:%M').time(), datetime.strptime('11:15', '%H:%M').time()),
    "12pm" : (datetime.strptime('11:45', '%H:%M').time(), datetime.strptime('12:15', '%H:%M').time()),
    "1pm" : (datetime.strptime('12:45', '%H:%M').time(), datetime.strptime('13:15', '%H:%M').time()),
    "2pm" : (datetime.strptime('13:45', '%H:%M').time(), datetime.strptime('14:15', '%H:%M').time()),
    "3pm" : (datetime.strptime('14:45', '%H:%M').time(), datetime.strptime('15:15', '%H:%M').time()),
    "4pm" : (datetime.strptime('15:45', '%H:%M').time(), datetime.strptime('16:15', '%H:%M').time()),
    "5pm" : (datetime.strptime('16:45', '%H:%M').time(), datetime.strptime('17:15', '%H:%M').time()),
    "6pm" : (datetime.strptime('17:45', '%H:%M').time(), datetime.strptime('18:15', '%H:%M').time())
}

# Return the current Perth time
def get_perth_time():
    utc_time = datetime.utcnow()
    perth_tz = pytz.timezone('Australia/Perth')
    perth_time = pytz.utc.localize(utc_time).astimezone(perth_tz)
    return perth_time

def set_session_form_select_options(form):

    # gets units for the facilitator (i.e. the current user)
    units = current_user.unitsFacilitate
    unit_choices = []
    for unit in units :
        # format with unitID as value, unitCode as option string name
        unit_choices.append((unit.unitID, unit.unitCode))

    session_name_choices = []
    session_time_choices = []

    if len(units) != 0 :
        # get session names for first unit
        session_names = units[0].sessionNames.split('|')
        for name in session_names :
            session_name_choices.append((name, name))

        # add empty session name default
        session_name_choices.append(('', ''))
        form.session_name.default = ''
        print(form.session_name.default)

        # get session times for first unit
        session_times = units[0].sessionTimes.split('|')
        for time in session_times :
            session_time_choices.append((time, time))

        time_suggestion = get_time_suggestion(session_times)
        
        if time_suggestion is None :
            # add empty default
            session_time_choices.append(('', ''))
            form.session_time.default = ''
            print(form.session_time.default)

        else :
            form.session_time.default = time_suggestion

        # set first unit as default
        form.unit.default = units[0].unitID

    else :
        print("User has no units to facilitate. Sending an empty form.")

    # set form options
    form.unit.choices = unit_choices
    form.session_name.choices = session_name_choices
    form.session_time.choices = session_time_choices

    form.submit.label.text = "Create"

    form.process()

def set_updatesession_form_select_options(current_session, current_unit, form):

    unit_choices = [(current_unit.unitID, current_unit.unitCode)]

    session_name_choices = []
    session_time_choices = []

    # get session names for unit
    session_names = current_unit.sessionNames.split('|')
    for name in session_names :
        session_name_choices.append(name)

    # get session times for unit
    session_times = current_unit.sessionTimes.split('|')
    for time in session_times :
        session_time_choices.append(time)
    
    # set form options
    form.unit.choices = unit_choices
    form.session_name.choices = session_name_choices
    form.session_time.choices = session_time_choices

    # set form defaults to current session
    form.unit.default = current_unit.unitID
    form.session_name.default = current_session.sessionName
    form.session_time.default = current_session.sessionTime

    form.submit.label.text = "Update"

    form.process()

def get_time_suggestion(session_times) :

    current_time = get_perth_time().time()
    print(f"current time: {current_time}")

    for session_time in session_times :
        if session_time in sessionTimeDefinitions :
            if current_time >= sessionTimeDefinitions[session_time][0] and current_time <= sessionTimeDefinitions[session_time][1] :
                print("suggesting {session_time} as likely time")
                return session_time

    print("no appropriate suggestions for time found")
    return None

def generate_student_info(student, attendance_record):

    login_status = "no" if attendance_record.signOutTime else "yes"
    
    student_info = {
        "name": f"{student.preferredName} {student.lastName}",
        "number": student.studentNumber,
        "id": student.studentID,
        "login": login_status,  
        "consent": student.consent,
        "signInTime": str(attendance_record.signInTime).split('.')[0], # this is because when I included the microseconds html's input type="time" wasn't formatting properly
        "signOutTime": str(attendance_record.signOutTime).split('.')[0],
        "grade": attendance_record.marks,
        "comments": "" if attendance_record.comments is None else attendance_record.comments
    }

    return student_info
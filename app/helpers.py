from datetime import datetime
import pytz
from flask_login import current_user

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
            session_name_choices.append(name)

        # get session times for first unit
        session_times = units[0].sessionTimes.split('|')
        for time in session_times :
            session_time_choices.append(time)

        # set first unit as default
        form.unit.default = units[0].unitID

    else :
        print("User has no units to facilitate. Sending an empty form.")

    # set form options
    form.unit.choices = unit_choices
    form.session_name.choices = session_name_choices
    form.session_time.choices = session_time_choices
    form.session_date.default = get_perth_time().date()

    form.submit.label.text = "Create"

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
    form.session_date.default = current_session.sessionDate

    form.submit.label.text = "Update"
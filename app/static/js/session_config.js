// register getSessionDetails function to fire when unit is selected
window.onload = function() {
    document.getElementById('unit').addEventListener("change", getSessionDetails)
}

// get the session names and session times for the unit
function getSessionDetails() {

    // gets the unit_id of the selected unit
    const unitCodeInputValue = document.getElementById('unit').value;

    // gets the session names and session times available for that unit
    fetch('/get_session_details/' + unitCodeInputValue).then(function(response) {
        response.json().then(function(data) {
            let session_name_optionHTML = '';
            let session_time_optionHTML = '';

            // creates the HTML to display the select field options
            for (let session_name of data.session_name_choices) {
                session_name_optionHTML += `<option value="${session_name}">${session_name}</option>`
            }
            
            for (let session_time of data.session_time_choices) {
                if (session_time == data.session_time_default) {
                    session_time_optionHTML += `<option selected value="${session_time}">${session_time}</option>`
                }
                else {
                    session_time_optionHTML += `<option value="${session_time}">${session_time}</option>`
                }
                
            }

            // inserts the HTML
            document.getElementById('session_name').innerHTML = session_name_optionHTML;
            document.getElementById('session_time').innerHTML = session_time_optionHTML;

        })
    })
}
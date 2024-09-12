window.onload = function() {
    document.getElementById('unit_code').addEventListener("change", getSessionDetails)
}

// gets the session names for the selected unit
function getSessionDetails() {
    const unitCodeInputValue = document.getElementById('unit_code').value;

    fetch('/get_session_details/' + unitCodeInputValue).then(function(response) {
        response.json().then(function(data) {
            let session_name_optionHTML = '';
            let session_time_optionHTML = '';

            for (let session_name of data.session_name_choices) {
                session_name_optionHTML += `<option value="${session_name}">${session_name}</option>`
            }
            
            for (let session_time of data.session_time_choices) {
                session_time_optionHTML += `<option value="${session_time}">${session_time}</option>`
            }

            document.getElementById('session_name').innerHTML = session_name_optionHTML;
            document.getElementById('session_time').innerHTML = session_time_optionHTML;

        })
    })
}
window.onload = function() {
    document.getElementById('unit_code').addEventListener("change", getSessionDetails)
}

// gets the session names for the selected unit
function getSessionDetails() {
    const unitCodeInputValue = document.getElementById('unit_code').value;

    fetch('/get_session_details/' + unitCodeInputValue).then(function(response) {
        response.json().then(function(data) {
            let session_name_optionHTML = '';
            let session_occurrence_optionHTML = '';

            for (let session_name of data.session_name_choices) {
                session_name_optionHTML += `<option value="${session_name}">${session_name}</option>`
            }
            
            for (let session_occurrence of data.session_occurrence_choices) {
                session_occurrence_optionHTML += `<option value="${session_occurrence}">${session_occurrence}</option>`
            }

            document.getElementById('session_name').innerHTML = session_name_optionHTML;
            document.getElementById('session_occurrence').innerHTML = session_occurrence_optionHTML;

        })
    })
}
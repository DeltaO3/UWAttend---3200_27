window.onload = function() {
    document.getElementById('unit_code').addEventListener("change", getSessionDetails)
}

// gets the session names for the selected unit
function getSessionDetails() {
    const unitCodeInputValue = document.getElementById('unit_code').value;

    fetch('/get_session_details/' + unitCodeInputValue).then(function(response) {
        response.json().then(function(data) {
            let optionHTML = '';

            for (let session_name of data.session_choices) {
                optionHTML += '<option value="' + session_name + '">' + session_name + "</option>"
            }
            document.getElementById('session_name').innerHTML = optionHTML;
        })
    })
}
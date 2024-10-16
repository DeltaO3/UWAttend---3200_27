//When submit button for session config form is clicked
$("#submit").click(function (e) {
	e.preventDefault();  // Prevent the default form submission

    checkSessionExists();

});

function checkSessionExists() {

    $.ajax({
        type: "POST",
        url: "/checksessionexists",
        data: $('form').serialize(),    // serialise the form's contents
        datatype: 'json',
        success: function(data) {
            // if the session already exists, show the warning modal
            if (data['result'] === "true") {

                const facilitatorNamesLength = data['facilitatorNames'].length;

                // if the session exists, but there are no students, immediately configure session
                if (facilitatorNamesLength == 0) {
                    submitSessionForm();
                }
                // if the session exists and has students signed in, say which facilitators have signed them in
                else {
                    let modalTextElement = $("#joinExistingSessionModalText").get(0);
                    modalTextElement.innerHTML = "You are joining an existing session with students signed in by: ";
                    for (let i = 0; i < facilitatorNamesLength; i++) {
                        modalTextElement.innerHTML += data['facilitatorNames'][i];
                        if (i != facilitatorNamesLength - 1) {
                            modalTextElement.innerHTML += ', ';
                        }
                    }
                    $('#joinExistingSessionModal').modal('show');
                }
            }
            // if the session doesn't exist, immediately configure session
            else if (data['result'] === "false") {
                submitSessionForm();
            }
            
            else if (data['result'] === "validateError") {
                
                const errorSpan = $("#errorMsg").get(0);
                errorSpan.innerHTML = "Please select a valid option for all fields."
                errorSpan.classList.remove("invisible");
            }
        },
        error: function(error) {
            console.error("Error configuring/updating session", error);
        }
    });

	return false; // Ensure no unexpected behaviour
}

function submitSessionForm() {

    // hide the modal (if there is one)
    $('#joinExistingSessionModal').modal('hide');

    // set route appropriately depending on whether form is to update or not
    let route = '';
    let update = $('form').attr('data-update');
    if (update == "true") {
        route = "/updatesession";
    }
    else {
        route = "/session";
    }

    $.ajax({
        type: "POST",
        url: route,
        data: $('form').serialize(),    // serialise the forms contents
        success: function() {
            window.location.href = '/home';  // Redirect to home after successfully configuring/updating session
        },
        error: function(error) {
            console.error("Error configuring/updating session", error);
        }
    });

	return false; // Ensure no unexpected behaviour

}
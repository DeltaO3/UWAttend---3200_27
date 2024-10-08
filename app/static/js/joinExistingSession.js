//When submit button for session config form is clicked
$("#submit").click(function (e) {
	e.preventDefault();  // Prevent the default form submission

    checkSessionExists();

});

function checkSessionExists() {

    $.ajax({
        type: "POST",
        url: "/checksessionexists",
        data: $('form').serialize(),    // serialise the forms contents
        datatype: 'json',
        success: function(data) {
            if (data['sessionExists'] === "true") {
                let modalTextElement = $("#joinExistingSessionModalText").get(0)

                const facilitatorNamesLength = data['facilitatorNames'].length

                if (facilitatorNamesLength == 0) {
                    modalTextElement.innerHTML = "You are joining an existing empty session.";
                }
                else {
                    modalTextElement.innerHTML = "You are joining an existing session with students signed in by: "
                    for (let i = 0; i < facilitatorNamesLength; i++) {
                        modalTextElement.innerHTML += data['facilitatorNames'][i];
                        if (i != facilitatorNamesLength - 1) {
                            modalTextElement.innerHTML += ', '
                        }
                    }
                }

                $('#joinExistingSessionModal').modal('show');
            }
            else if (data['sessionExists'] === "false") {
                submitSessionForm();
            }
        },
        error: function(error) {
            console.error("Error configuring session", error);
        }
    });

	return false; // Ensure no unexpected behaviour
}

function submitSessionForm() {

    $('#joinExistingSessionModal').modal('hide');

    $.ajax({
        type: "POST",
        url: "/session",
        data: $('form').serialize(),    // serialise the forms contents
        success: function() {
            window.location.href = '/home';  // Redirect to home after successfully configuring session
        },
        error: function(error) {
            console.error("Error configuring session", error);
        }
    });

	return false; // Ensure no unexpected behaviour

}
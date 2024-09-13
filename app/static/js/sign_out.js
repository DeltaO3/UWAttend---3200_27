//Runs when attendance form is submitted - put post request to flask in here
$("#signOutButton").click(function (e) {
	e.preventDefault();  // Prevent the default form submission

    $("#signOutModal").modal('show');
	
	return false;
});

function SignAllOut() {

    $('#signOutModal').modal('hide');

    var sessionID = $("#session_id").val();

    $.ajax({
        type: "POST",
        url: "/sign_all_out",
        data: {
            sessionID: sessionID  // Send the session ID to the backend
        },
        success: function(response) {
            // Handle successful sign out, e.g., redirect to home or show a message
            window.location.href = '/';  // Redirect to home after sign out
        },
        error: function(error) {
            console.error("Error signing out students:", error);
        }
    });

	return false; // Ensure no unexpected behaviour
}
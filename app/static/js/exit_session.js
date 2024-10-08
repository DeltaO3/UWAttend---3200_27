//When exit session button is clicked
$("#exitSessionButton").click(function (e) {
	e.preventDefault();  // Prevent the default form submission

    $("#exitSessionModal").modal('show');
	
	return false;
});

function exitSession() {

    $('#exitSessionModal').modal('hide');

    $.ajax({
        type: "GET",
        url: "/exitSession",
        success: function() {
            window.location.href = '/session';  // Redirect to session config after exiting session
        },
        error: function(error) {
            console.error("Error exiting session", error);
        }
    });

	return false; // Ensure no unexpected behaviour

}
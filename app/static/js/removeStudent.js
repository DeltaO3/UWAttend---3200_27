//Runs when remove student form is submitted - put post request to flask in here
$("#remove_from_session_form").submit(function (e) {
	e.preventDefault();  // Prevent the default form submission
    
	$("#removeStudentModal").modal('show');
    console.log("here")
	return false;
});

//Calls an ajax function to a backend route, passing the consent in JSON format
function removeStudent() {
	// Submit the form
    console.log("Student is to be removed");
    
    $("#remove_from_session_form").off("submit").submit(); 
    
    $("#consentModal").modal('hide');

	return false; // Ensure no unexpected behaviour
}
//Runs when attendance form is submitted - put post request to flask in here
$("#attendanceForm").submit(function (e) {
	e.preventDefault();  // Prevent the default form submission

	// Only display the modal if consent has not been previously granted 
	if ($("#hidden_consent_indicator").val() == "yes") {
		$("#consentModal").modal('show');
		document.getElementById('hidden_consent_indicator').value = "no";
	} else {
		addAttendance();
	}
	return false;
});

//Calls an ajax function to a backend route, passing the consent in JSON format
function addAttendance(consent = "none") {

	// Set the consent value in the hidden field
    $("#consent_status").val(consent);

    // Log the consent for testing
    console.log("Consent was given: " + consent);

    // Close the modal before submitting
    $("#consentModal").modal('hide');

	console.log("Final Consent Status: " + $("#consent_status").val());

    // Submit the form after setting the consent status
    $("#attendanceForm").off("submit").submit();  // Ensure the form is submitted this time

	return false; // Ensure no unexpected behaviour
}
//Runs when attendance form is submitted - put post request to flask in here
$("#attendanceForm").submit(function (e) {
	$("#consentModal").modal('show');
	return false;
});
//Runs when attendance form is submitted - put post request to flask in here
$("#attendanceForm").submit(function (e) {
	//TODO: add conditional to check - if consent already given, then run the function:
	//addAttendance()
	//TODO: else (no consent), open modal
	$("#consentModal").modal('show');
	return false;
});

//Calls an ajax function to a backend route, passing the consent in JSON format
function addAttendance(consent = "none") {
	//Purely for testing, remove when implementing proper backend connection.
	if (consent == "yes") {
		console.log("consent was given! ");
	}

	/*Can add data from form to this JSON instead of flaskform if desired, 
	using the following commented code (delete this comment when decided on method):
	student = $("#studentSignIn").val()*/
	let sendData = { "consent": consent }

	//Call backend route for attendance with consent - currently uses placeholder backend call,
	//replace with desired url and copy code from placeholder url to get consent
	$.ajax({
		type: "POST",
		url: "/add_student",
		dataType: "json",
		contentType: "application/json",
		data: JSON.stringify(sendData)
	}).always(function (data) {
		location.reload(true);
	});
}
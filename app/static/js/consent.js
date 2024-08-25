//Runs when attendance form is submitted - put post request to flask in here
$("#attendanceForm").submit(function (e) {
	$("#consentModal").modal('show');
	return false;
});

function addAttendance(consent = "none") {
	//Purely for testing, remove when implementing proper backend connection.
	if (consent == "yes") {
		console.log("consent was given! ");
	}
	let sendData = { "consent": consent }

	//Call backend route for attendance with consent - placeholder backend call
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
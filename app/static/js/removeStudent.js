function removeStudent(id) {
	// Submit the form
    console.log("Student ID: " + id);
    
    $("#removeStudentModal").modal('hide');

    window.location.href = '/remove_from_session?student_id=' + id

    // redirect to remove student with student information

	return false; // Ensure no unexpected behaviour
}

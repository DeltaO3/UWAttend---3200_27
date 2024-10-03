function exitSession() {

    $.ajax({
        type: "GET",
        url: "/exitSession",
        success: function() {
            // Handle successful sign out, e.g., redirect to home or show a message
            window.location.href = '/session';  // Redirect to session config after exiting session
        },
        error: function(error) {
            console.error("Error signing out students:", error);
        }
    });

	return false; // Ensure no unexpected behaviour

}
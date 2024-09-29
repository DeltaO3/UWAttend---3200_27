// Function to update the current time
function updateTime() {
    // Time displayed on webpage
    const timeElementDisplay = document.getElementById('current_time_display');
    // Time for backend
    const timeElementHidden = document.getElementById('current_time');
    // Retrieve current Perth time string from the data attribute
    let perthTimeStr = timeElementDisplay.getAttribute('data-perth-time');

    // Convert and increment time for live feedback
    let perthTime = new Date(perthTimeStr);
    perthTime.setSeconds(perthTime.getSeconds() + 1);

    // Format to human readable
    const formattedTime = perthTime.toLocaleTimeString();

    // Update the displayed time
    timeElementDisplay.textContent = formattedTime;
    timeElementHidden.value = formattedTime;

    // Convert back to ISO string so it can be used in the next update
    const newPerthTimeStr = perthTime.toISOString();
    timeElementDisplay.setAttribute('data-perth-time', newPerthTimeStr);
}

// Function to check the server status
function checkServerStatus() {
    fetch('/ping')
        .then(response => {
            if (response.ok) {
                // If server is running, do nothing
            } else {
                // If server is down, show an alert
                ShowAlert("Warning: The server has disconnected!", "danger");
            }
        })
        .catch(error => {
            // If fetch fails (server down or disconnected), show an alert
            ShowAlert("Warning: The server has disconnected!", "danger");
        });
}

function ShowAlert(message, type) {
    const alertDiv = document.getElementById('serverAlert');
    alertDiv.textContent = message;
    alertDiv.className = `alert alert-${type}`; // Sets the type (success, danger, etc.)
    alertDiv.style.display = 'block'; // Show the alert

    // Automatically hide the alert after a few seconds
    setTimeout(() => {
        alertDiv.style.display = 'none';
    }, 7000);
}


// Run code only on /session
if (window.location.href.indexOf("session") != -1) {
    // Update the time every second
    setInterval(updateTime, 1000);
    // Initial call to display the time immediately when the page loads
    updateTime();
}

// Check server status every 5 seconds
setInterval(checkServerStatus, 2000);
// Initial check when the page loads
checkServerStatus();



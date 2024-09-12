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

// Function to update the database name dynamically
function updateDatabaseName() {
    const unitCodeInput = document.getElementById('unit_code');
    // const semesterInput = document.getElementById('semester');

    // UpperCase handling for unit code and semester
    unitCodeInput.value = unitCodeInput.value.toUpperCase();
    // semesterInput.value = semesterInput.value.toUpperCase();

    const unitCode = unitCodeInput.value;
    const sessionName = document.getElementById('session_name').value;
    // const semester = semesterInput.value;
    const currentYear = new Date().getFullYear();

    // Calculate semester based on the current month
    const currentMonth = new Date().getMonth() + 1;
    let semester = "SEM2";
    if (currentMonth <= 6) {
        semester = "SEM1";
    }

    if (unitCode && sessionName) {
        const databaseName = `${unitCode}_${semester}_${currentYear}`;
        document.getElementById('database_name_display').textContent = databaseName;
    } else {
        document.getElementById('database_name_display').textContent = '';
    }
}

// Run code only on /session
if (window.location.href.indexOf("session") != -1) {
    // Update the time every second
    setInterval(updateTime, 1000);

    // Initial call to display the time immediately when the page loads
    updateTime();

}

// Function to update the current time
function updateTime() {
    // Time displayed on webpage
    const timeElementDisplay = document.getElementById('session_time_display');
    // Time for backend
    const timeElementHidden = document.getElementById('session_time');

    const now = new Date();
    const formattedTime = now.toLocaleTimeString();

    timeElementDisplay.textContent = formattedTime;
    timeElementHidden.value = formattedTime;
}

// Function to update the database name dynamically
function updateDatabaseName() {
    const unitCodeInput = document.getElementById('unit_code');
    const semesterInput = document.getElementById('semester');

    // UpperCase handling for unit code and semester
    unitCodeInput.value = unitCodeInput.value.toUpperCase();
    semesterInput.value = semesterInput.value.toUpperCase();

    const unitCode = unitCodeInput.value;
    const sessionName = document.getElementById('session_name').value;
    const semester = semesterInput.value;
    const currentYear = new Date().getFullYear();

    if (unitCode && sessionName && semester) {
        const databaseName = `${unitCode}_${semester}_${currentYear}`;
        document.getElementById('database_name_display').textContent = databaseName;
    } else {
        document.getElementById('database_name_display').textContent = '';
    }
}

// Update the time every second
setInterval(updateTime, 1000);

// Initial call to display the time immediately when the page loads
updateTime();

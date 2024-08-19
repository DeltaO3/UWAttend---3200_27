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
    if (currentMonth <= 5) {
        semester = "SEM1";
    }

    if (unitCode && sessionName) {
        const databaseName = `${unitCode}_${semester}_${currentYear}`;
        document.getElementById('database_name_display').textContent = databaseName;
    } else {
        document.getElementById('database_name_display').textContent = '';
    }
}

// Function to validate form inputs
function validateConfig(event) {
    const unitCodeInput = document.getElementById('unit_code');
    const sessionNameInput = document.getElementById('session_name');
    // const semester = document.getElementById('semester').value.toUpperCase();

    const unitCode = unitCodeInput.value.toUpperCase();
    const sessionName = sessionNameInput.value;

    let isValid = true;
    let errorMessage = '';

    // Reset error states
    unitCodeInput.classList.remove('input-error');
    sessionNameInput.classList.remove('input-error');

    if (!validSessions.includes(sessionName)) {
        isValid = false;
        errorMessage += 'Invalid session name. ';
        sessionNameInput.classList.add('input-error');

    }
    if (!validUnitCodes.includes(unitCode)) {
        isValid = false;
        errorMessage += 'Invalid unit code. ';
        unitCodeInput.classList.add('input-error');
    }
//  if (!validSemesters.includes(semester)) {
//      isValid = false;
//      errorMessage += 'Invalid semester. ';
//  }

    if (!isValid) {
        alert(errorMessage);  // Show a popup alert with the error message
        event.preventDefault();  // Prevent form submission
    }

}

// Run code only on /session
if (window.location.href.indexOf("session") != -1) {
    // Update the time every second
    setInterval(updateTime, 1000);

    // Initial call to display the time immediately when the page loads
    updateTime();

    // Add event listener to validate configuration menu form on submission
    document.querySelector('form').addEventListener('submit', validateConfig);
}

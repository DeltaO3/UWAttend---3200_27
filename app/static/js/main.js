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
    const unitCode = document.getElementById('unit_code').value.toUpperCase();
    const sessionName = document.getElementById('session_name').value;
    // const semester = document.getElementById('semester').value.toUpperCase();

    let isValid = true;
    let errorMessage = '';

    if (!validSessions.includes(sessionName)) {
        isValid = false;
        errorMessage += 'Invalid session name. ';
    }
    if (!validUnitCodes.includes(unitCode)) {
        isValid = false;
        errorMessage += 'Invalid unit code. ';
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

// Need to combine these two if statements to one at some point... Is there a way to check if a webpage is specifically "session.html"????
// Check if we are on a page with a session time display
if (document.getElementById('session_time_display') && document.getElementById('session_time')) {
    // Update the time every second
    setInterval(updateTime, 1000);

    // Initial call to display the time immediately when the page loads
    updateTime();
}

// Check if form exists before adding event listener
if (document.querySelector('form')){
    // Add event listener to validate configuration menu form on submission
    document.querySelector('form').addEventListener('submit', validateConfig);
}

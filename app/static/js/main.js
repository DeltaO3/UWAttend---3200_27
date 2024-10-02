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

// Run code only on /session
if (window.location.href.indexOf("session") != -1) {
    // Update the time every second
    setInterval(updateTime, 1000);

    // Initial call to display the time immediately when the page loads
    updateTime();

}

//Works only on reload, but I doubt a user will be changing colour schemes and not expecting to have to reload
if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    $(".modal").attr("data-bs-theme", "dark");
    $(".navbar").attr("data-bs-theme", "dark");
    $(".form-check-input").attr("data-bs-theme", "dark");
    $(".form-control-file").attr("data-bs-theme", "dark");
    $(".form-select-parent").attr("data-bs-theme", "dark");
}

//Closes an alert 3 seconds after it pops up
setTimeout(function () {
    $('.alert').alert('close');
}, 3000); 
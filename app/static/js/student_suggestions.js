document.addEventListener('DOMContentLoaded', function () {
    const studentInput = document.getElementById('student_search');
    const suggestionsContainer = document.getElementById('suggestions_container');
    
    if (studentInput) {

        studentInput.addEventListener('input', function () {
            const query = studentInput.value.trim().toLowerCase();
            
            if (query.length > 0) {
                // Send an AJAX request to the server to get student suggestions
                fetch(`/student_suggestions?q=${encodeURIComponent(query)}`)
                    .then(response => response.json())
                    .then(data => {
                        displaySuggestions(data);
                    })
                    .catch(error => {
                        console.error('Error fetching student suggestions:', error);
                    });
            } else {
                clearSuggestions();
            }
        });

        function displaySuggestions(suggestions) {
            clearSuggestions();
        
            suggestions.forEach(suggestion => {
                const suggestionItem = document.createElement('a');
                suggestionItem.classList.add('list-group-item');
                suggestionItem.textContent = `${suggestion.name} (${suggestion.number})`;
                suggestionItem.setAttribute('data-student-id', suggestion.number);  // Store student ID
                suggestionItem.setAttribute('signed-in', suggestion.signedIn); // Store signed in status
                if (suggestion.signedIn == 1) {
                    suggestionItem.style.backgroundColor = 'lightcoral'; 
                } else {
                    suggestionItem.style.backgroundColor = 'lightgreen'; 
                }

                document.getElementById('hidden_consent_indicator').value = "no";
                document.getElementById('studentID').value = false;
        
                suggestionItem.addEventListener('click', function () {
                    // Set the student ID and name when a suggestion is clicked
                    document.getElementById('studentID').value = suggestion.id;

                    // Do not ask for consent if student's consent is already yes or not required
                    if (suggestion.consentNeeded == "yes" || suggestion.consentNeeded == "not required") {

                        document.getElementById('hidden_consent_indicator').value = "no";
                    } else {
                        document.getElementById('hidden_consent_indicator').value = "yes";
                    }
                    
                    studentInput.value = suggestion.name;

                    clearSuggestions();
                });
        
                suggestionsContainer.appendChild(suggestionItem);
            });
        }

        function clearSuggestions() {
            suggestionsContainer.innerHTML = '';
        }
    }
});

function redirectToStudent(studentId) {
    // Find the form for the specific student and submit it
    document.getElementById('studentForm_' + studentId).submit();
}

$(document).ready(function() {
    $('#search-bar').on('input', function() {
        let query = $(this).val().toLowerCase();
        
        $('.table-element').each(function() {
            let studentName = $(this).find('span').eq(0).text().toLowerCase(); 
            let studentID = $(this).find('span').eq(1).text().toLowerCase();   
            
			// By doing it this way - the original ordering of the list should be preserved (so don't have to re-sort later)
            if (studentName.includes(query) || studentID.includes(query)) {
                $(this).show();  
            } else {
                $(this).hide();  
            }
        });
    });
});

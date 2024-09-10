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
                suggestionItem.classList.add('list-group-item', 'list-group-item-action', 'suggestion-item');
                suggestionItem.textContent = `${suggestion.name} (${suggestion.number})`;
                suggestionItem.setAttribute('data-student-id', suggestion.number);  // Store student ID
        
                suggestionItem.addEventListener('click', function () {
                    // Set the student ID and name when a suggestion is clicked
                    document.getElementById('studentID').value = suggestion.id;
                    document.getElementById('session_id').value = 1;
                    
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

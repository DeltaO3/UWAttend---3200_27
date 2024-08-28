document.addEventListener('DOMContentLoaded', function () {
    const studentInput = document.getElementById('student_search');
    const suggestionsContainer = document.getElementById('suggestions_container');
    
    if (studentInput) {
        // Placeholder data
        const students = [
            { name: "alex", id: "12345678" },
            { name: "bob", id: "87654321" },
            { name: "cathy", id: "22224444" },
            { name: "catherine", id: "33335555" },
            { name: "charlie", id: "44446666" },
            { name: "caterina", id: "55557777" },
            { name: "grace", id: "66668888" },
            { name: "harry", id: "77779999" },
        ];

        studentInput.addEventListener('input', function () {
            const query = studentInput.value.trim().toLowerCase();
            
            if (query.length > 0) {
                const filteredStudents = students.filter(student => 
                    student.name.toLowerCase().includes(query) || student.id.includes(query)
                );
                displaySuggestions(filteredStudents);
            } else {
                clearSuggestions();
            }
        });

        function displaySuggestions(suggestions) {
            clearSuggestions();
        
            suggestions.forEach(suggestion => {
                const suggestionItem = document.createElement('a');
                suggestionItem.classList.add('list-group-item', 'list-group-item-action');
                suggestionItem.textContent = `${suggestion.name} (${suggestion.id})`;
        
                suggestionItem.addEventListener('click', function () {
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

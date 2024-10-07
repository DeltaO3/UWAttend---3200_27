window.onload = function () {
    const comment_node = document.getElementById("comments")
    comment_node.textContent = comment_node.getAttribute("data-comment")

}

function removeStudent(id) {
    // Submit the form
    console.log("Student ID: " + id);

    $("#removeStudentModal").modal('hide');

    window.location.href = '/remove_from_session?student_id=' + id

    // redirect to remove student with student information

    return false; // Ensure no unexpected behaviour
}

$(document).ready(function () {
    const commentSuggestions = [];
    $('.suggestion').each(function () {
        commentSuggestions.push($(this).text())
    })

    $('.suggestion').on('click', function () {
        var suggestedText = $(this).attr('id');
        var commentsField = $('#comments');

        commentsField.val(function (i, text) {
            return text + (text ? ', ' : '') + suggestedText;
        });
    });



    $('#comments').on("change keyup paste", function () {
        let inputString = $('#comments').val();
        console.log(inputString);
        commentSuggestions.forEach(element => {
            if (inputString.indexOf(element) >= 0) {
                $('#' + element).fadeToggle("fast", "linear")
            }
        });
    })
});
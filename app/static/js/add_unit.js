$("#commentsenabled").change(function () {
	if (this.checked) {
		$("#comment-suggestions-parent").removeClass("d-none")
	} else {
		$("#comment-suggestions-parent").addClass("d-none")
	}
})

function removeSessions(thisObj) {
	sessionText = thisObj.attr("id");
	sessionsArray = $("#sessions").val().split("|");
	console.log(sessionsArray)
	index = sessionsArray.indexOf(sessionText)
	sessionsArray.splice(index, 1)
	newString = sessionsArray.join("|")
	console.log(newString)
	thisObj.fadeOut("fast", "linear", function () { thisObj.remove(); });
	$("#sessions").val(newString)
}


function removeComments(thisObj) {
	commentText = thisObj.attr("id");
	commentsArray = $("#comments").val().split("|");
	console.log(commentsArray)
	index = commentsArray.indexOf(commentText)
	commentsArray.splice(index, 1)
	newString = commentsArray.join("|")
	console.log(newString)
	thisObj.fadeOut("fast", "linear", function () { thisObj.remove(); });
	$("#comments").val(newString)
}

$(window).on("load", function () {
	if ($("#commentsenabled").prop("checked")) {
		$("#comment-suggestions-parent").removeClass("d-none");
	} else {
		$("#comment-suggestions-parent").addClass("d-none");
	}

	//Load any data in hidden forms
	sessionsArray = $("#sessions").val().split("|");
	sessionsArray.forEach(element => {
		newBadge = $("<span class='badge session-badge p-2' id='" + element + "'></span>").text(element);
		$("#sessions-container").append(newBadge);
	});

	commentsArray = $("#comments").val().split("|");
	commentsArray.forEach(element => {
		newBadge = $("<span class='badge comment-badge p-2' id='" + element + "'></span>").text(element);
		$("#comments-container").append(newBadge);
	});
})

$(document).ready(function () {
	//Input for session names
	$("#sessionnames").on("keypress", function (e) {
		if (e.which == 13) {
			e.preventDefault();
			if ($("#sessionnames").val()) {
				curr = $("#sessions").val();
				input = $("#sessionnames").val()
				curr = curr + "|" + input;
				$("#sessionnames").val("");
				//remove redundant |
				if (curr.charAt(0) === '|') {
					curr = curr.substring(1);
				}
				$("#sessions").val(curr);
				console.log($("#sessions").val());
				newBadge = $("<span class='badge session-badge p-2' id='" + input + "'></span>").text(input);
				newBadge.on("click", function () {
					removeSessions($(this));
				})
				$("#sessions-container").append(newBadge);
			}
		}
	})

	$(".session-badge").on("click", function () {
		removeSessions($(this));
	})

	//Input for comments
	$("#commentsuggestions").on("keypress", function (e) {
		if (e.which == 13) {
			e.preventDefault();
			if ($("#commentsuggestions").val()) {
				curr = $("#comments").val();
				input = $("#commentsuggestions").val()
				curr = curr + "|" + input;
				$("#commentsuggestions").val("");
				//remove redundant |
				if (curr.charAt(0) === '|') {
					curr = curr.substring(1);
				}
				$("#comments").val(curr);
				console.log($("#comments").val());
				newBadge = $("<span class='badge comment-badge p-2' id='" + input + "'></span>").text(input);
				newBadge.on("click", function () {
					removeComments($(this));
				})
				$("#comments-container").append(newBadge);
			}
		}
	})

	$(".comment-badge").on("click", function () {
		removeComments($(this));
	})
})
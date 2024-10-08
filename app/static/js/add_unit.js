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
	index = sessionsArray.indexOf(sessionText)
	sessionsArray.splice(index, 1)
	newString = sessionsArray.join("|")
	console.log(newString)
	thisObj.fadeOut("fast", "linear", function () { thisObj.remove(); });
	$("#sessions").val(newString)
}

$(window).on("load", function () {
	if ($("#commentsenabled").prop("checked")) {
		$("#comment-suggestions-parent").removeClass("d-none")
	} else {
		$("#comment-suggestions-parent").addClass("d-none")
	}

	sessionsArray = $("#sessions").val().split("|")
	sessionsArray.forEach(element => {
		newBadge = $("<span class='badge session-badge p-2' id='" + element + "'></span>").text(element);
		$("#sessions-container").append(newBadge);
	});
})

$(document).ready(function () {
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
})
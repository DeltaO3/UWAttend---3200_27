$("#commentsenabled").change(function () {
	if (this.checked) {
		$("#comment-suggestions-parent").removeClass("d-none")
	} else {
		$("#comment-suggestions-parent").addClass("d-none")
	}
})

$(window).on("load", function () {
	if ($("#commentsenabled").prop("checked")) {
		$("#comment-suggestions-parent").removeClass("d-none")
	} else {
		$("#comment-suggestions-parent").addClass("d-none")
	}
})
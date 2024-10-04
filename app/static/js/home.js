function resize_table() {
	usedHeight = 0;
	rect = $("#classTable")[0].getBoundingClientRect();
	usedHeight += rect.top;
	usedHeight += $(".home-footer").height();
	//Arbitrary small amount of pixels for wiggle room at bottom
	remainingHeight = window.innerHeight - usedHeight - 10
	$("#classTable").height(remainingHeight + "px")
}

$(window).on("load resize", function () {
	resize_table();
})

$(".alert").on("closed.bs.alert", function () {
	resize_table();
})
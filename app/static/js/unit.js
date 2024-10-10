function resize_table() {
	usedHeight = 0;
	rect = $("#unitTable")[0].getBoundingClientRect();
	usedHeight += rect.top;
	console.log(usedHeight)
	//Arbitrary small amount of pixels for wiggle room at bottom
	remainingHeight = window.innerHeight - usedHeight - 10
	$("#unitTable").height(remainingHeight + "px")
}

$(window).on("load resize", function () {
	resize_table();
})

$(".alert").on("closed.bs.alert", function () {
	resize_table();
})
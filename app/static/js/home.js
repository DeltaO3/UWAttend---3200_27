
$(window).on("load resize", function () {
	usedHeight = 0;
	rect = $("#classTable")[0].getBoundingClientRect();
	console.log(rect.top)
	usedHeight += rect.top;
	usedHeight += $(".home-footer").height();
	//Arbitrary small amount of pixels for wiggle room at bottom
	remainingHeight = window.innerHeight - usedHeight - 10
	console.log("total" + window.innerHeight + "used" + usedHeight + "remaining" + remainingHeight)
	$("#classTable").height(remainingHeight + "px")
})

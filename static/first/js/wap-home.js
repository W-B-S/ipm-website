$(window).scroll(function () {
	if ($(window).scrollTop() > 0) {
		$('#top-bar').addClass('active')
	} else {
		$('#top-bar').removeClass('active')
	}
})

$('#nav-button').on('click', function(){
	$('#nav').toggleClass('active');
});

$('a', '#nav').on('click', function(){
	if ($(this).index() === 0) {
		$('html, body').animate({
			scrollTop: 0
		}, 300);
	} else if ($(this).index() === 1) {
		$('html, body').animate({
			scrollTop: $('#brief').offset().top - 120
		}, 300);
	} else if ($(this).index() === 2) {
		$('html, body').animate({
			scrollTop: $('#advantage').offset().top - 120
		}, 300);
	} else if ($(this).index() === 3) {
		$('html, body').animate({
			scrollTop: $('#scenes').offset().top - 120
		}, 300);
	}
	$('#nav').removeClass('active')
})

$('a', '#scenes .btn-box').on('click', function(){
	$('a', '#scenes .btn-box').removeClass('active')
	$('.msg-box', '#scenes').css('display', 'none')
	$('.scenes-pic', '#scenes').css('display', 'none')
	$(this).addClass('active')
	$('.msg-box', '#scenes').eq($(this).index()).css('display', 'block')
	$('.scenes-pic', '#scenes').eq($(this).index()).css('display', 'inline-block')
})
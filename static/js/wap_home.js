$(window).scroll(function () {
	if ($(window).scrollTop() > 0) {
		$('#top-bar').addClass('active')
	} else {
		$('#top-bar').removeClass('active')
	}
})

$('#nav-button').on('click', function(){
	$(this).css('display', 'none');
	$('#nav').css('display', 'block').animate({
		right: 0
	});
});

$('li', '#nav').on('click', function(){
	if ($(this).index() === 0) {
		$('html, body').animate({
			scrollTop: 0
		}, 300);
	} else if ($(this).index() === 1) {
		$('html, body').animate({
			scrollTop: $('#brief-info').offset().top - 60
		}, 300);
	} else if ($(this).index() === 2) {
		$('html, body').animate({
			scrollTop: $('#advantage').offset().top - 60
		}, 300);
	} else if ($(this).index() === 3) {
		$('html, body').animate({
			scrollTop: $('#team').offset().top - 60
		}, 300);
	} else if ($(this).index() === 4) {
		$('html, body').animate({
			scrollTop: $('#investors').offset().top - 60
		}, 300);
	}
	$('#nav').animate({
		right: -$('#nav').width()
	}, function(){
		$('#nav').css('display', 'none');
	});
	$('#nav-button').css('display', 'block');
})
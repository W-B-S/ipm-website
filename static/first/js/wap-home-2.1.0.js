$(document).ready(function(){
	// 自定义弹窗
	(function() {
	  var f, c, g;
	  function b(h) {
	    g = $("#float_info")[0];
	    if (!g) {
	      g = document.createElement("div");
	      g.id = "float_info";
	      g.className = "err_popo";
	      g.innerHTML = '<span id="float_info_msg"></span>';
	      document.body.appendChild(g)
	    }
	    f && window.clearTimeout(f);
	    a(1, h || "出现错误");

	      var i = document.documentElement || document.body;
	      g.style.top = (document.documentElement.scrollTop||document.body.scrollTop) + ((document.documentElement.clientHeight || document.body.clientHeight) - g.offsetHeight) / 2 + "px"

	    f = window.setTimeout(function() {
	        a(0)
	      },
	      2000)
	  }
	  function a(j, h) {
	    var i = g,
	      l = 0,
	      k = 20;
	    h && ($("#float_info_msg").html(h));
	    if (j) {
	      i.style.opacity = "0";
	      i.style.display = "block";
	      c && window.clearInterval(c);
	      c = window.setInterval(function() {
	          if (l == 10) {
	            window.clearInterval(c)
	          }
	          l++;
	          i.style.opacity = 0.1 * l
	        },
	        k)
	    } else {
	      c && window.clearInterval(c);
	      c = window.setInterval(function() {
	          if (l == 10) {
	            window.clearInterval(c);
	            i.style.display = "none"
	          }
	          l++;
	          i.style.opacity = 0.1 * (10 - l)
	        },
	        k)
	    }
	  }
	  window.salert = b
	})();

	// 窗口禁止&&恢复滚动
	var scrollTop = 0;
	var BODYBOX = {
	  _noScroll: function(scrollTop) {
	    $('body').css({
	      'overflow': 'hidden',
	      'position': 'fixed',
	      'top': scrollTop * -1
	    });

	  },
	  _reScroll: function(scrollTop) {
	    $('body').css({
	      'overflow': 'auto',
	      'position': 'static',
	      'top': 'auto'
	    })
	    $('html, body').scrollTop(scrollTop);
	  }
	};

	var flag = true
	var isFirst = true
	$(window).scroll(function () {
		if ($(window).scrollTop() > 0) {
			$('#top-bar').addClass('active')
			if (flag) {
				$('#float-bar-player-fix, #float-bar-player').addClass('active')
			}
			setTimeout(function () {
				flag = true
			}, 1000)
		} else {
			$('#top-bar').removeClass('active')
			$('#float-bar-player-fix, #float-bar-player').removeClass('active')
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

	// 播放器放大缩小
	$('#toggle').on('click', function(){
		$('#float-bar-player-fix, #float-bar-player').toggleClass('active')
		if (!$('#float-bar-player-fix, #float-bar-player').hasClass('active')) {
			flag = false
		}
	})

	// 关闭广告
	$('#close-bar-ad').on('click', function(){
		$(this).parent().remove()
	})

	// 邮箱地址弹窗
	$('#share-email').on('click', function(e) {
		scrollTop = $(window).scrollTop();
		$('#mask').height($(document).height())
		$('#mask, #email-address').css('display', 'block')
		BODYBOX._noScroll(scrollTop)
	})

	// 微信地址弹窗
	$('#share-wechat').on('click', function(e) {
		scrollTop = $(window).scrollTop();
		$('#mask').height($(document).height())
		$('#mask, #wechat-address').css('display', 'block')
		BODYBOX._noScroll(scrollTop)
	})

	// 播放链接弹窗
	$('#copy-link-btn').on('click', function(){
		scrollTop = $(window).scrollTop();
		$('#mask, #player-link').css('display', 'block')
		$('#player-link').css('top', $(window).scrollTop() + 100)
		$('#mask').height($(document).height())
		BODYBOX._noScroll(scrollTop)
	})

	// 注册弹窗
	$('#get-gold-btn').on('click', function(){
	    scrollTop = $(window).scrollTop();
		$('#appoint, #appoint-result').css('display', 'none')
		$('#valid-mobile').css('display', 'block')
		$('#progress-line-box').removeClass('active')

		$('#mask, #register').css('display', 'block')
		$('#register').css('top', $(window).scrollTop() + 100)
		$('#mask').height($(document).height())
		BODYBOX._noScroll(scrollTop)
	})

	// 下一步
	$('#next-btn').on('click', function(){
		if (/^[0-9]{1,20}$/.test($('#mobile').val())) {
			$.ajax({
				url: '/api/v1/invitation/search',
				type: 'post',
				data: {
					mobile: $('#mobile').val()
				},
				success: function(response) {
					if (response.status === 0) {
						$('span', '#mobile-text').text(response.data.mobile)
						$('#valid-mobile, #appoint-result').css('display', 'none')
						$('#appoint').css('display', 'block')
						$('#progress-line-box').addClass('active')
					} else if (response.status === 1) {
						$('#quick-copy2').attr('data-clipboard-text', '听区块链歌曲，还能领积分，点击：' + response.data.link)
										 .text(response.data.link)
						$('#valid-mobile, #appoint').css('display', 'none')
						$('#appoint-result').css('display', 'block')
						$('#progress-line-box').addClass('active')
						// 预约过
						$('.success-tips', '#appoint-result').text('该手机号已预约过').addClass('active')
					} else {
						salert(response.msg)
					}
				},
				error: function() {
					salert('网络连接失败，请稍后重试...')
				}
			})
		} else {
			salert('请输入正确的手机号码')
		}
	})

	// 预约领取
	$('#appoint-btn').on('click', function(){
		if (!(/^\w+[-+.\w]*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/.test($('#email').val()))) {
			salert('请输入正确的邮箱地址');
			return false;
		} else {
			$.ajax({
				url: '/api/v1/invitation/create',
				type: 'post',
				data: {
					mobile: $('#mobile').val(),
					address: $('#email').val(),
					path: window.location.href
				},
				success: function(response) {
					if (response.status === 0) {
						$('#quick-copy2').attr('data-clipboard-text', '听区块链歌曲，还能领积分，点击：' + response.data.link)
										 .text(response.data.link)
						$('#valid-mobile, #appoint').css('display', 'none')
						$('#appoint-result').css('display', 'block')
						$('#progress-line-box').addClass('active')
						// 未预约过
						$('.success-tips', '#appoint-result').text('已预约成功').removeClass('active')
					} else {
						salert(response.msg)
					}
				},
				error: function() {
					salert('网络连接失败，请稍后重试...')
				}
			})
			
		}
	})

	// 预约领取返回上一步
	$('.go-back').on('click', function(){
		$('#appoint, #appoint-result').css('display', 'none')
		$('#valid-mobile').css('display', 'block')
		$('#progress-line-box').removeClass('active')
	})

	// 关闭弹窗
	$('.close-btn, #mask').on('click', function(){
		BODYBOX._reScroll(scrollTop)
		$('#mask, #player-link, #register, #email-address, #wechat-address').css('display', 'none')
	})

	// 一键复制
	var clipboard1 = new ClipboardJS('.quick-copy1')  
	clipboard1.on('success', function(e) {  
	    salert("复制成功！")  
	})
	clipboard1.on('error', function(e) {  
	    salert("复制失败,请手动复制")  
	})

	var clipboard2 = new ClipboardJS('.quick-copy2', {
		text: function () {
			return $('#quick-copy2').attr('data-clipboard-text')
		}
	})  
	clipboard2.on('success', function(e) {  
	    salert("复制成功！")  
	})
	clipboard2.on('error', function(e) {  
	    salert("复制失败,请手动复制")  
	})

	// 音乐播放

	//转换音频时长显示
	function transTime(time) {
	    var duration = parseInt(time);
	    var minute = parseInt(duration/60);
	    var sec = duration%60+'';
	    var isM0 = ':';
	    if(minute == 0){
	        minute = '00';
	    }else if(minute < 10 ){
	        minute = '0'+minute;
	    }
	    if(sec.length == 1){
	        sec = '0'+sec;
	    }
	    return minute+isM0+sec
	}

	//更新进度条
	function updateProgress(audio) {
	    var value = Math.round((Math.floor(audio.currentTime) / Math.floor(audio.duration)) * 100, 0);
	    $('#current-progress').css('width', value + '%');
	    $('#current-time').html(transTime(audio.currentTime));
	}

	var audio = document.getElementById('audio-tag');

	// 控制播放暂停
	$('#control-btn').click(function(){
        if(audio.paused){
            audio.play();
            $(this).addClass('active')
            if (isFirst) {
            	isFirst = false
            	salert('音频加载中，请耐心等待...')
            }
        } else{
            audio.pause();
            $(this).removeClass('active')
        }
    })

    $('#audio-tag').on("loadeddata",function () {
        $('#total-time').text(transTime(this.duration));
    });

    audio.addEventListener('timeupdate', function(){
    	updateProgress(audio)
    }, false);

    // 拖动进度条
    var pgsWidth = $('#progress').width();
    $('#progress').click(function (e) {
        var rate = (e.offsetX - ($(this).width()-pgsWidth)/2)/pgsWidth;
        audio.currentTime = audio.duration * rate;
        updateProgress(audio);
    });

    // 播放结束
    $('#audio-tag').on('ended', function () {
    	$('#control-btn').removeClass('active');
    });
})

























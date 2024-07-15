$('.open-popup').click(function (e) {
    e.preventDefault();
    $('.popup-bg').fadeIn()
});

$('.close-popup').click(function () {
    $('.popup-bg').fadeOut()
});

// Page loading animation
$(window).on('load', function() {
    $('#js-preloader').addClass('loaded');
});

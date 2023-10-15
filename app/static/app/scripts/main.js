$('.open-popup').click(function (e) {
    e.preventDefault();
    $('.popup-bg').fadeIn()
});

$('.close-popup').click(function () {
    $('.popup-bg').fadeOut()
});

$('.hide-js').hide();
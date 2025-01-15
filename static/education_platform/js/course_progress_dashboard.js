$(document).ready(function () {
    $('.promo-banner-wrapper').click(function (e) {
        e.preventDefault();
        // Перейти по ссылке которая внутри именно этого блока
        var link = $(this).find('a').attr('href');
        if (link) {
            // Перейти по ссылке
            window.location.href = link;
        }
    });
});
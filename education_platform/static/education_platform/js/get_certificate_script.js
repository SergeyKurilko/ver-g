$(document).ready(function () {
    
    // Отображение loader пока не загрузился сертификат (он генерируется) "на лету"

    // Находим мето, где будет изображение по ID
    var $img = $('#certificateImage');

    // Виджеты "поделиться" изначально d-none
    var certificateShare = $('.certificate-share')

    // Находим loader по классу
    var $loader = $('.image-loader-place');


    $img.on('load', function() {
        $loader.addClass('d-none');
        certificateShare.removeClass('d-none');
    });

    var owlCarouselAboutCertificatedsText = $(".owl-about-certificates-text").owlCarousel({
        /* nav: true, */
        margin: 0,
        dotsEach: 1,
        autoplay:true,
        autoplayTimeout:3000,
        autoplaySpeed: 1000,
        loop:true,
        /* autoHeight:true, */
        autoplayHoverPause:true,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 1
            },
            1000: {
                items: 1
            }
        }
    })
});
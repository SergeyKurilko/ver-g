$(document).ready(function () {
    // Корректировка стилей выпадающего меню в navbar
    $('#EducationPlatformNavbarMenuButton').click(function (e) {
        if ($(this).attr('aria-expanded') === 'true') {
            $('#loginButtonEducationPlatform').removeClass('ms-3');
            $('#authButtonGroup').addClass('mt-2');
            $('.dropdown-profile-menu').addClass('min').removeClass('max');
        } else if ($(this).attr('aria-expanded') === 'false') {
            $('#loginButtonEducationPlatform').addClass('ms-3');
            $('#authButtonGroup').removeClass('mt-2');
            $('.dropdown-profile-menu').addClass('max').removeClass('min');
        }
    });

    // Функция для получения параметра из URL
    function getUrlParameter(name) {
        var urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(name);
    }

    // Помещаем значение параметра filter в переменную
    var filterParam = getUrlParameter('filter')

    // Если в строке запроса был параметр фильтра, то находим нужную
    // Кнопку фильтрации в DOM и присваиваем ей класс .my-courses-filter-button-activate
    // Кнопки фильтров помечены id с идентичными названиями возможных параметров filter (all, completed, incompleted)
    if (filterParam) {
        $(`#filter-${filterParam}`).addClass('my-courses-filter-button-activate')
    }

    var owlCarouselRecommendedCourses = $('.owl-carousel-recommended-courses').owlCarousel({
        margin: 10,
        dotsEach: 1,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 2
            },
            1000: {
                items: 3
            }
        }
    })
    $('.next-course-card-owl-button').click(function () {
        owlCarouselRecommendedCourses.trigger('next.owl.carousel');
    })

    var owlCarouselLatestArticles = $(".owl-latest-articles").owlCarousel({
        nav: true,
        margin: 0,
        dotsEach: 1,
        autoplay:true,
        autoplayTimeout:3000,
        autoplaySpeed: 1000,
        loop:true,
        autoHeight:true,
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
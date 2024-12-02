$(document).ready(function () {
    /* $('#EducationPlatformNavbarMenuButton').click(function (e) { 
        if ($(this).attr('aria-expanded') === 'true') {
            $('#loginButtonEducationPlatform').removeClass('ms-3');
            $('#authButtonGroup').addClass('mt-2');
            $('.dropdown-profile-menu').addClass('min').removeClass('max');
        } else if ($(this).attr('aria-expanded') === 'false') {
            $('#loginButtonEducationPlatform').addClass('ms-3');
            $('#authButtonGroup').removeClass('mt-2');  
            $('.dropdown-profile-menu').addClass('max').removeClass('min');
        }
    }); */
   

    var owlCarouselCoursesHomepage = $('.owl-carousel-latest-courses').owlCarousel({
        margin:10,
  /*       nav:true, */
        dotsEach: 1,
        responsive:{
            0:{
                items:1
            },
            600:{
                items:2
            },
            1000:{
                items:3
            }
        }
    })
    $('.next-course-card-owl-button').click(function() {
        owlCarouselCoursesHomepage.trigger('next.owl.carousel');
    })

    var owlCarouselCoursePacksHomepage = $('.owl-carousel-latest-course-packs').owlCarousel({
        margin:10,
/*         nav:true, */
        dotsEach: 1,
        responsive:{
            0:{
                items:1
            },
            600:{
                items:2
            },
            1000:{
                items:3
            }
        }
    })
    $('.next-course-pack-card-owl-button').click(function() {
        owlCarouselCoursePacksHomepage.trigger('next.owl.carousel');
    })
    

});
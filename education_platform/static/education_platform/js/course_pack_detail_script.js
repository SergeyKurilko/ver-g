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

    //Из шаблона получаем переменные: UpArrow, DownArrow, CourseId, GetCourseUrl
    //раскладывание и складывание курсов в пакете курсов
    $('.show-hidden-courses').click(function (e) {
        e.preventDefault();
        var idForCourseBlock = $(this).attr('id').slice(23);

        var courseBlock = $(`#coursesForPack${idForCourseBlock}`);


        if (courseBlock.hasClass('d-none')) {
            // Если у courseBlock есть класс d-none, удаляем его и меняем иконку на DownArrowIcon
            courseBlock.removeClass('d-none');
            $(this).html(UpArrow);
        } else {
            // Если у lessonBlock нет класса d-none, добавляем его и меняем иконку на UpArrowIcon
            courseBlock.addClass('d-none');
            $(this).html(DownArrow);
        }
    });



    //Отслеживаем нажатие кнопки (купить курс)
    $(`.get_course_button`).click(function (e) {
        e.preventDefault();
        $.ajax({
            type: "GET",
            url: GetCoursePackUrl,
            dataType: "json",
            success: function (response) {
                // Если пользователь не авторизован, открываем форму авторизации/регистрации
                if (response.success === 'not_authenticated') {
                    var NotAuthenticatedModal = new bootstrap.Modal(document.getElementById('notAuthenticatedModal'));
                    NotAuthenticatedModal.show();

                    // Получение формы оплаты пакета курсов
                } else if (response.success === 'payment_course_pack_form') {
                    var modalForPaymentFormHtml = response.payment_course_pack_form_modal
                    $('.get-paid-course-modal-place').html(modalForPaymentFormHtml)
                    // Открываем modal через bootstrap'овский метод modal
                    $('#modalForPaidCoursePack').modal('show')
                }
            }
        });
    });

    //Если пользователь пытается получить курс не зарегистрировавшись, то в модальном окне выбирает вход или регистрация

    //нажатие "войти"
    $(`#loginFromGetCourse`).click(function (e) {
        e.preventDefault();
        $(`#notAuthenticatedModalCloseButton`).trigger("click");
        $('#loginButtonEducationPlatform').trigger('click');
    });

    $(`#registerFromGetCourse`).click(function (e) {
        e.preventDefault();
        $(`#notAuthenticatedModalCloseButton`).trigger("click");
        $('#registerButtonEducationPlatform').trigger('click');
    });
});
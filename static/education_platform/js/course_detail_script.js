$(document).ready(function () {
    var permissionToSendPromo = false

    // Корректировка стилей выпадающего меню navbar
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
    //раскладывание и складывание уроков у модуля
    $('.show-hidden-lessons').click(function (e) {
        e.preventDefault();
        var idForLessonBlock = $(this).attr('id').slice(31);
        var lessonBlock = $(`#lessonsForBlock${idForLessonBlock}`);

        if (lessonBlock.hasClass('d-none')) {
            // Если у lessonBlock есть класс d-none, удаляем его и меняем иконку на DownArrowIcon
            lessonBlock.removeClass('d-none');
            $(this).html(UpArrow);
        } else {
            // Если у lessonBlock нет класса d-none, добавляем его и меняем иконку на UpArrowIcon
            lessonBlock.addClass('d-none');
            $(this).html(DownArrow);
        }
    });

    //Отслеживаем нажатие кнопки (купить/или/пройти курс)
    $(`.get_course_button`).click(function (e) {
        e.preventDefault();
        $.ajax({
            type: "GET",
            url: GetCourseUrl,
            dataType: "json",
            success: function (response) {
                if (response.success === 'not_authenticated') {
                    var NotAuthenticatedModal = new bootstrap.Modal(document.getElementById('notAuthenticatedModal'));
                    NotAuthenticatedModal.show();

                    // Логика получения бесплатного курса
                } else if (response.success === 'access_to_course_is_created') {
                    location.reload();
                } else if (response.success === 'access_to_course_already_exist') {
                    location.reload();
                    // Если курс платный
                } else if (response.success === 'course_is_paid') {
                    var urlForGetPaidCourse = response.url_for_get_paid_course

                    // Получив информацию о том, что курс платный, получаем так же
                    // URL на который надо сделать запрос, чтобы получить форму оплаты
                    $.ajax({
                        type: "GET",
                        url: urlForGetPaidCourse,
                        dataType: "json",
                        success: function (response) {
                            // В ответе получаем модельное окно с формой оплаты
                            if (response.success === 'payment_course_form') {
                                var modalForPaymentFormHtml = response.payment_course_form_modal
                                $('.get-paid-course-modal-place').html(modalForPaymentFormHtml)
                                // Открываем modal через bootstrap'овский метод modal
                                $('#modalForPaidCourse').modal('show')

                                // В открытом новом окне убираем поле $('.promo-input')
                                var promoInputContainer = $('.promo-input-container')
                                promoInputContainer.hide()

                                // Отслеживание ввода промокода

                                // Показ поля с вводом промокода 
                                $('#havePromoCheck').change(function (e) {
                                    e.preventDefault();
                                    if ($(this).prop('checked')) {
                                        promoInputContainer.show(300);
                                    } else (promoInputContainer.hide(300))
                                });

                                // Отслеживание количества символов в поле promo
                                $('#promoCode').on('input', function (e) {
                                    if ($(this).val().length === 8) {
                                        $('.promo-button').removeClass('ver-g-disabled-button');
                                        permissionToSendPromo = true
                                        
                                    } else {
                                        $('.promo-button').addClass('ver-g-disabled-button');
                                        permissionToSendPromo = false
                                    }
                                });


                                // Отслеживание отправки промокода, отправку делаем, только если permissionToSendPromo is true
                                $('#usePromoCodeForm').submit(function (e) {
                                    
                                        e.preventDefault();
                                        if (permissionToSendPromo) {
                                        $.ajax({
                                            type: "POST",
                                            url: $(this).attr('action'),
                                            data: $(this).serialize() + `&course_pk=${$('input[name="product_id"]').val()}`,
                                            dataType: "json",
                                            success: function (response) {
    
                                                // Если после применения промокода осталась сумма к оплате
                                                if (response.status === 'ok' && response.type_of_access === 'discounted') {
                                                    var oldPrice = parseFloat(response.old_price);
                                                    var newPrice = parseFloat(response.new_price);
                                                    var promoCode = response.promo_code_pk
    
                                                    $('#promoCode').removeClass('is-invalid')
                                                    $('#promoCodeFeedback').remove();
    
                                                    $('#promoCode').addClass('is-valid')
                                                    $('#promoCode').attr('readonly', true)
    
    
                                                    $('input[name="amount"]').attr('value', newPrice)
                                                    $('.amount-value-col').html(
                                                        `
                                                        <div class="d-flex align-items-center">
                                                        <span class="price-without-discount">${oldPrice} ₽</span> 
                                                        <span class="ms-2" style="color: red; font-size: 1.5rem;">${newPrice} ₽</span>
                                                        `
                                                    )
                                                    $('input[name="havePromoCode"]').addClass('d-none');
                                                    $('label[for="havePromoCheck"]').addClass('d-none')
                                                    $('.promo-button').addClass('d-none')
                                                    $('#promoCode').after(`<span style="color: green">Промокод действителен! ${response.validity_period}</span>`)
                                                    $(`<input type="hidden" name="promo_code" value="${promoCode}">`).insertBefore($('input[name="product_type"]'))
                                                }
                                                // Если промокод был на скидку 100% и amont == 0
                                                else if (response.status === 'ok' && response.type_of_access === 'is_free') {
                                                    console.log('Логика получения доступа со 100% скидкой')
                                                    var oldPrice = parseFloat(response.old_price);
                                                    var newPrice = parseFloat(response.new_price);
                                                    var promoCode = response.promo_code_pk
                                                    var urlForGetCourseFreeWithPromo = response.url_for_get_course_free_with_promo
    
                                                    $('#promoCode').removeClass('is-invalid')
                                                    $('#promoCodeFeedback').remove();
    
                                                    $('#promoCode').addClass('is-valid')
                                                    $('#promoCode').attr('readonly', true)
                                                    $('input[name="amount"]').attr('value', newPrice)
                                                    $('.amount-value-col').html(
                                                        `
                                                        <div class="d-flex align-items-center">
                                                        <span class="price-without-discount">${oldPrice} ₽</span> 
                                                        <span class="ms-2" style="color: red; font-size: 1.5rem;">${newPrice} ₽</span>
                                                        `
                                                    )
                                                    $('.promo-button').addClass('d-none')
                                                    $('#promoCode').after(`<span style="color: green">Промокод действителен! ${response.validity_period}</span>`)
    
                                                    // Заменяем action у формы оплаты (#paidForm), и заменяем контент кнопки с "оплатить" на "получить бесплатно"
                                                    $('#paidForm').attr('action', urlForGetCourseFreeWithPromo)
                                                    $(`<input type="hidden" name="promo_code" value="${promoCode}">`).insertBefore($('input[name="product_type"]'))
                                                    $('#paidFormSuccessButton').html('Получить бесплатно')
    
                                                    // Получив стоимость равную 0, заменив action у формы оплаты, отслеживаем ее отправку:
                                                    $('#paidForm').submit(function (e) {
                                                        e.preventDefault();
    
                                                        $.ajax({
                                                            type: "POST",
                                                            url: $(this).attr('action'),
                                                            data: $(this).serialize(),
                                                            dataType: "json",
                                                            success: function (response) {
                                                                if (response.status === 'ok') {
                                                                    var htmlForInsertInModal = response.html_for_render
    
                                                                    $('#modalBody').html(htmlForInsertInModal)
                                                                }
                                                            }
                                                        });
                                                    });
                                                }
                                                // Если проверка промокода не прошла
                                                else if (response.status === 'error') {
                                                    console.log(response.error_message)
                                                    $('#promoCode').addClass('is-invalid')
                                                    $('#promoCodeFeedback').html(response.error_message)
                                                }
    
                                            }
                                        });
                                    }
                                    

                                });
                            }
                        }
                    });
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
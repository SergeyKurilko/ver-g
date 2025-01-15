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

    let fileDialogOpened = false;


    // Загрузка аватара

    $('#uploadAvatarButton').click(function (e) { // отслеживаем нажатие "Загрузить аватар"
        e.preventDefault();
        // Показываем overlay
        $('.overlay').removeClass("d-none");
        $('.overlay').addClass("d-flex");

        // Устанавливаем флаг, что окно выбора файла было открыто
        fileDialogOpened = true;

        $('#avatarInput').click(); // Инициируем клик input для запуска проводника 

    });

    // В случае закрытия окна выбора файла
    var avatarInput = document.getElementById('avatarInput')
    avatarInput.addEventListener('cancel', () => {
        $('.overlay').addClass("d-none");
      });



    // Отслеживаем выбор файла в проводнике (в открытом input (avatarInput))
    $('#avatarInput').change(function (e) {
        e.preventDefault();

        // Проверим расширение файла, чтобы не отправлялись файлы, которые НЕ jpg, jpeg, png
        var file = this.files[0];

        // Проверяем расширение файла
        var allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;
        if (!allowedExtensions.test(file.name)) {
            alert('Недопустимый формат файла. Разрешены только изображения (jpg, jpeg, png).');
            // Очищаем выбор файла
            $('#avatarInput').val('');

            // Убираем overlay
            $('.overlay').addClass("d-none");
            return;
        }


        // При выборе файла отправляем ajax

        var urlForUploadAvatarAjax = $('#avatarUploadForm').attr("action")
        var avatarUploadFormData = new FormData($('#avatarUploadForm')[0]);

        $.ajax({
            type: "POST",
            url: urlForUploadAvatarAjax,
            data: avatarUploadFormData,
            processData: false,
            contentType: false,
            dataType: "json",
            success: function (response) {
                if (response.status === "success") {
                    location.reload()
                }
                // Ответ time_error приходит, если запрос отправляется чаще, чем раз в минуту
                else if (response.status === "time_error") {
                    // Убираем overlay
                    $('.overlay').addClass("d-none");

                    $('#avatarErrorPlace').remove();
                    $('#uploadAvatarButton').remove();
                    $('#avatarInput').after(`<span id="avatarErrorPlace" class="ps-0 mt-2 text-center" style="color: red">${response.message}</span>`);
                    $('#avatarErrorPlace').animate({ opacity: 1 }, 500);
                }
            }
        });
    });

    // Отслеживаем, если пользователь закрыл проводник без выбора файла
    $(document).on('focusin', function (e) {
        e.preventDefault();

        // Проверяем, было ли открыто окно выбора файла и не был ли выбран файл
        if (fileDialogOpened && !$('#avatarInput').val()) {
            // Убираем overlay
            $('.overlay').addClass("d-none");
            // Сбрасываем флаг
            fileDialogOpened = false;
        }
    });





    // Обработка формы изменения личных данных
    $('#firstNameInput').click(function (e) {
        $(this).removeClass("text-muted")
    });

    $('#lastNameInput').click(function (e) {
        $(this).removeClass("text-muted")
    });

    $('#emailInput').click(function (e) {
        $(this).removeClass("text-muted")
    });

    // При расфокусировке
    $('#firstNameInput').blur(function (e) {
        $(this).addClass("text-muted")
    });

    $('#lastNameInput').blur(function (e) {
        $(this).addClass("text-muted")
    });

    $('#emailInput').blur(function (e) {
        $(this).addClass("text-muted")
    });

    // Отслеживание отправки формы изменений личных данных
    $('#updatePersonalDataForm').submit(function (e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: $(this).attr("action"),
            data: $(this).serialize(),
            dataType: "json",
            success: function (response) {
                if (response.status === "success") {
                    // Показываем overlay
                    $('.overlay').removeClass("d-none");
                    $('.overlay').addClass("d-flex");
                    location.reload()
                }
                // Ответ time_error, если слишком частый запрос, то выводим сообщение ошибки и отсключаем кнопку
                else if (response.status === "time_error" || response.status === "edit_limit_error") {
                    $('.updateErrorPlace').removeClass("d-none");
                    $('.updateErrorPlace').html(`<span class="ps-0" style="color: red">${response.message}</span>`);
                    $('.updateErrorPlace').animate({ opacity: 1 }, 500);
                    $('#updatePersonalDataButton').attr("disabled", true)

                    // Ответ email-error, если поле пустое или такая почта уже зарегистрирована
                } else if (response.status === "email-error") {

                    $('#emailErrorPlace').remove();
                    $('.email_input').after(`<span id="emailErrorPlace" class="ps-0" style="color: red">${response.message}</span>`);
                    $('#emailErrorPlace').animate({ opacity: 1 }, 500);
                }
            }
        });
    });


});
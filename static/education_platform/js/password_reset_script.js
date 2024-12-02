$(document).ready(function () {

    //Отслеживание нажатия кнопки Напомнить пароль, чтобы закрыть окно login
    $('#passwordResetEducationPlatform').click(function (e) { 
        //Инициируем "нажатие" кнопки закрытия модального окна с формой логина.
        $('#closeLoginFormButton').trigger('click');
    });

    //Отслеживание отправки формы сброса пароля
    var passwordResetForm = $('#passwordResetForm')

    passwordResetForm.submit(function (e) { 
        e.preventDefault();
        var email = $('#emailResetPassword').val()

        $.ajax({
            type: "POST",
            url: passwordResetForm.attr('action'),
            data: passwordResetForm.serialize(),
            dataType: "json",
            success: function (response) {
                if (response.status === 'success') {
                    $('#modalBodyForPasswordResetForm').html(`
                        <div class="container">Мы отправили вам письмо на адрес: ${email}. 
                        Напишите нам, если вы не получили его в течение нескольких минут:  
                        <a href="mailto:info@ver-g.ru">info@ver-g.ru</a>
                        </div>
                        `)
                } else if (response.status === 'error') {
                    var passwordResetFormErrorList = response.password_reset_form_errors

                    $.each(passwordResetFormErrorList, function (fieldName, errorTextList) { 
                        var errorField = $('#emailResetPassword')
                        var matchFeedback = $('#' + fieldName + 'MatchFeedback');
                        var errorText = '';

                        $.each(errorTextList, function (indexInArray, valueOfElement) { 
                            errorText += valueOfElement + '<br>'
                        });

                        if (matchFeedback.length === 1) {
                            errorField.addClass('is-invalid')
                            errorField.after(matchFeedback.html(`${errorText}`))
                        }
                    });
                }
            }
        });
    });

    //Часть скрипта для формы установки нового пароля
    var resetPasswordConfirmForm = $('#studentPasswordResetConfirmForm');

    $(resetPasswordConfirmForm).submit(function (e) { 
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: resetPasswordConfirmForm.attr('action'),
            data: resetPasswordConfirmForm.serialize(),
            dataType: "json",
            success: function (response) {
                if (response.status === 'success') {
                    $('#containerForPasswordResetConfirm').html(`
                        <h4>Пароль успешно изменен.</h4>
                        <div>Сейчас Вы будете перенаправлены на главную страницу, где сможете войти с новым паролем.</div>
                        `)

                        setTimeout(function() {
                            window.location.href = response.success_url;
                        }, 2000);
                    

                } else if (response.status === 'error') {
                    var ResetPasswordErrorsList = response.reset_password_form_errors

                    $.each(ResetPasswordErrorsList, function (fieldName, errorTextList) { 
                        var errorField = $(`#id_${fieldName}`);
                        var matchFeedback = $('#' + fieldName + 'MatchFeedback');
                        var errorText = '';

                        $.each(errorTextList, function (indexInArray, valueOfElement) { 
                            errorText += valueOfElement + '<br>'
                        });

                        if (matchFeedback.length === 1) {
                            errorField.addClass('is-invalid')
                            errorField.after(matchFeedback.html(`${errorText}`))
                        }
                    });
                }
            }
        });
    });
    



});
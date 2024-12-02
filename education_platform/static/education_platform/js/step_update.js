$(document).ready(function () {

    // Переменные из шаблона: has_question, has_many_answers, next_step_ajax_url
    // Переменная has_question = false, если в шаге нет вопроса, true, если вопрос есть.
    // Переменная has_many_correct_answers содержит True, если у вопроса несколько правильных ответов, False, если правильный ответ один и None, если вопроса нет
    // Переменная next_step_ajax_url содержит url для view, обрабатывающий ajax



    // Если step содержит вопрос:
    if (has_question === 'True') {

        // отключаем кнопку "Следующий шаг" и делаем ее невидимой
        $('#nextStep').attr('disabled', true)
        $('#nextStep').addClass('d-none');

        //Проверяем один ли правильный ответ у вопроса или несколько

        // Если правильный ответ один:
        if (has_many_correct_answers === 'False') {

            // Отслеживаем нажатие чекбоксов. При выборе другого, снимаем отметку с другого нажатого и активируем кнопку отправить.
            $('input[name="answer"]').change(function () {
                // Снимаем отметку со всех чекбоксов, кроме текущего
                $('input[name="answer"]').not(this).prop('checked', false);

                // Проверяем, есть ли хотя бы один отмеченный чекбокс
                var anyChecked = $('input[name="answer"]:checked').length > 0;

                // Активируем или деактивируем кнопку отправки
                $('#sendAnswerButton').prop('disabled', !anyChecked)
            });


            // Отслеживание отправки формы с ответами постом.
            $('#formForQuestion').submit(function (e) {
                e.preventDefault();
                // сохраняем форму (данные):
                var formData = $(this).serialize();
                // сохраняем pk вопроса для проверки ответов во view
                var questionPk = $(this).attr('question-pk');

                $.ajax({
                    type: "POST",
                    url: next_step_ajax_url,
                    data: formData + '&question_pk=' + questionPk,
                    dataType: "json",
                    success: function (response) {
                        if (response.status === 'correct_answer') {


                            //отключаем кнопку "отправить"
                            $('#sendAnswerButton').prop('disabled', true)

                            // возвращаем кнопку "Следующий шаг" и делаем ее невидимой
                            $('#nextStep').attr('disabled', false)
                            $('#nextStep').removeClass('d-none');
                            $('#nextStep').click(function (e) {
                                e.preventDefault();
                                $('.overlay').show();
                                $('.blinking_text_and_logo_loader').removeClass('d-none')

                                // у кнопки есть атрибут current-step в котором из django подтянут pk текущего шага
                                var currentStep = $(this).attr('current-step')
                                // Отправка ajax
                                $.ajax({
                                    type: "GET",
                                    url: next_step_ajax_url,

                                    // отправляем так же и pk текущего шага в принимающий view
                                    data: {
                                        'current_step': currentStep
                                    },
                                    dataType: "json",
                                    success: function (response) {
                                        if (response.status === 'ok') {
                                            setTimeout(function () {
                                                location.reload();
                                            }, 1000);
                                        }
                                    }
                                });
                            });

                        }
                    }
                });
            });
        }



        // если правильный ответ не один
        else if (has_many_correct_answers === 'True') {

            // отслеживаем нажатие чекбоксов
            $('input[name="answer"]').change(function (e) {
                // если нажат хотя бы один чекбокс
                var anyChecked = $('input[name="answer"]:checked').length > 0;

                //то делаем кнопку отправить доступной
                $('#sendAnswerButton').prop('disabled', !anyChecked)

            });

            $('#sendAnswerButton').click(function (e) {
                e.preventDefault();
                // сохраняем форму:
                var formData = $('#formForQuestion');
                // сохраняем pk вопроса
                var questionPk = formData.attr('question-pk');

                $.ajax({
                    type: "POST",
                    url: next_step_ajax_url,
                    data: formData.serialize() + '&question_pk=' + questionPk,
                    dataType: "json",
                    success: function (response) {
                        if (response.status === 'correct_answers') {
                            // 'ok' возвращается, если ответы правильные. возвращаем доступ к кнопке "Следующий шаг"
                            $('#nextStep').attr('disabled', false)
                            $('#nextStep').removeClass('d-none');

                            // Отключаем кнопку "отправить"
                            $('#sendAnswerButton').attr('disabled', true)

                            // Отслеживаем нажатие "Следующий шаг"
                            $('#nextStep').off('click').on('click', function (e) {
                                e.preventDefault();
                                // воспроизводим экран загрузки
                                $('.overlay').show();
                                $('.blinking_text_and_logo_loader').removeClass('d-none')

                                // определяем текущий шаг
                                var currentStep = $(this).attr('current-step')
                                // отправляем ajax для перехода на следующий шаг
                                $.ajax({
                                    type: "GET",
                                    url: next_step_ajax_url,
                                    data: {
                                        'current_step': currentStep
                                    },
                                    dataType: "json",
                                    success: function (response) {
                                        if (response.status === 'ok') {
                                            setTimeout(function () {
                                                location.reload();
                                            }, 1000);
                                        }
                                    }
                                });
                            })

                        } else if (response.status === 'wrong_answers') {
                            // Если ответы неправильные


                        }
                    }
                });
            });
        }



        // Если step не содержит вопрос    
    } else if (has_question === 'False') {
        // Отслеживание нажатия кнопки "Следующий шаг"
        // переменная next_step_ajax_url передается из v
        $('#nextStep').click(function (e) {
            e.preventDefault();
            $('.overlay').show();
            $('.blinking_text_and_logo_loader').removeClass('d-none')

            // у кнопки есть атрибут current-step в котором из django подтянут pk текущего шага
            var currentStep = $(this).attr('current-step')
            // Отправка ajax
            $.ajax({
                type: "GET",
                url: next_step_ajax_url,

                // отправляем так же и pk текущего шага в принимающий view
                data: {
                    'current_step': currentStep
                },
                dataType: "json",
                success: function (response) {
                    if (response.status === 'ok') {
                        setTimeout(function () {
                            location.reload();
                        }, 1000);
                    }
                }
            });
        });

    }


    //Поведение боковой панели

    //Переменная isPinned меняется при нажатии кнопки "закрепить"
    var isPinned = false;

    //При наведении на кнопку .a-side_total_steps_open_button
    $(".a-side_total_steps_open_button").hover(function () {
        if (!isPinned) {
            //Если "закрепить" не нажато, то
            //Добавляем боковой панели .a-side_total_steps_wrapper доп. класс open 
            //Этот класс в css меняет transform: translateX(-100%); на translateX(0);
            //Т.е. панель "выезжает слева направо"
            $(".a-side_total_steps_content_wrapper").addClass("open")
            $('.a-side_total_steps_open_button').addClass("hidden")
            $('.a-side_total_steps_content_pin-button').removeClass("d-none")
            $('.a-side_total_steps_open_button span').text("")
        }
    });


    // При покидании мышкой зоны a-side_total_steps_wrapper, если не нажато "Закрепить", то убираем класс open
    // и панель снова возвращается влево
    $('.a-side_total_steps_content_wrapper').mouseleave(function () { 
        if (!isPinned) {
            $(this).removeClass("open")
            $('.a-side_total_steps_open_button').removeClass('hidden')
            $('.a-side_total_steps_content_pin-button').addClass("d-none")
            $('.a-side_total_steps_open_button span').text("Содержание")
        }
    });

    var fixedPinContent = `<span>Открепить</span> <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pin" viewBox="0 0 16 16">
  <path d="M4.146.146A.5.5 0 0 1 4.5 0h7a.5.5 0 0 1 .5.5c0 .68-.342 1.174-.646 1.479-.126.125-.25.224-.354.298v4.431l.078.048c.203.127.476.314.751.555C12.36 7.775 13 8.527 13 9.5a.5.5 0 0 1-.5.5h-4v4.5c0 .276-.224 1.5-.5 1.5s-.5-1.224-.5-1.5V10h-4a.5.5 0 0 1-.5-.5c0-.973.64-1.725 1.17-2.189A6 6 0 0 1 5 6.708V2.277a3 3 0 0 1-.354-.298C4.342 1.674 4 1.179 4 .5a.5.5 0 0 1 .146-.354m1.58 1.408-.002-.001zm-.002-.001.002.001A.5.5 0 0 1 6 2v5a.5.5 0 0 1-.276.447h-.002l-.012.007-.054.03a5 5 0 0 0-.827.58c-.318.278-.585.596-.725.936h7.792c-.14-.34-.407-.658-.725-.936a5 5 0 0 0-.881-.61l-.012-.006h-.002A.5.5 0 0 1 10 7V2a.5.5 0 0 1 .295-.458 1.8 1.8 0 0 0 .351-.271c.08-.08.155-.17.214-.271H5.14q.091.15.214.271a1.8 1.8 0 0 0 .37.282"/>
</svg>`

    var unfixedPinContent = `<span>Закрепить</span> <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pin-angle" viewBox="0 0 16 16">
  <path d="M9.828.722a.5.5 0 0 1 .354.146l4.95 4.95a.5.5 0 0 1 0 .707c-.48.48-1.072.588-1.503.588-.177 0-.335-.018-.46-.039l-3.134 3.134a6 6 0 0 1 .16 1.013c.046.702-.032 1.687-.72 2.375a.5.5 0 0 1-.707 0l-2.829-2.828-3.182 3.182c-.195.195-1.219.902-1.414.707s.512-1.22.707-1.414l3.182-3.182-2.828-2.829a.5.5 0 0 1 0-.707c.688-.688 1.673-.767 2.375-.72a6 6 0 0 1 1.013.16l3.134-3.133a3 3 0 0 1-.04-.461c0-.43.108-1.022.589-1.503a.5.5 0 0 1 .353-.146m.122 2.112v-.002zm0-.002v.002a.5.5 0 0 1-.122.51L6.293 6.878a.5.5 0 0 1-.511.12H5.78l-.014-.004a5 5 0 0 0-.288-.076 5 5 0 0 0-.765-.116c-.422-.028-.836.008-1.175.15l5.51 5.509c.141-.34.177-.753.149-1.175a5 5 0 0 0-.192-1.054l-.004-.013v-.001a.5.5 0 0 1 .12-.512l3.536-3.535a.5.5 0 0 1 .532-.115l.096.022c.087.017.208.034.344.034q.172.002.343-.04L9.927 2.028q-.042.172-.04.343a1.8 1.8 0 0 0 .062.46z"/>
</svg>`

    $('.a-side_total_steps_content_pin-button').click(function() {
        isPinned = !isPinned;
        $(this).html(isPinned ? fixedPinContent : unfixedPinContent);
    });



});
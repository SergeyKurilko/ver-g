$(document).ready(function () {
    // Скрипт загружается после входа пользователя в step_detail
    // Из шаблона передаются переменные stepHasQuestions, progressPk, total_steps_in_course, urlForMakeStepIsCompleted, csrfToken, question_has_many_correct_answers
    // Переменная question_has_many_correct_answers = True, если у вопроса несколько правильных ответов и False, если 1 ответ правильный

    // Функция, если курс завершен из обычного шага (в котором нет вопроса). Т.е. прохождение последнего шага привело к его завершению
    function course_complete_from_simple_step(modalHTML) {

        $('.modal_place').html(modalHTML)

        console.log('Готовимся к рендеру кнопки Это последний шаг курса')

        // рендерим кнопку для вызова модального окна с сообщением о завершении курса
        var buttonForShowModal = `
        <div style="font-weight: 500; font-size: large;">Это последний шаг курса.</div>
        <button id="CourseCompleteFromSimpleStepButton" type="button" class="btn btn-success mt-2" data-toggle="modal" data-target="#courseCompleteModal">
        Завершить курс
        </button>
        `

        // размещаем кнопку вместо навигационных кнорок
        $('.step_navigation_buttons_content').html(buttonForShowModal)

        // Далее, отслеживаем нажатие этой кнопки, чтобы открывать модальное окно
        $('#CourseCompleteFromSimpleStepButton').click(function (e) { 
            e.preventDefault();
            
            $('#courseCompleteModal').modal('show')
        });


    }

    // Функция, если курс завершен из шага с вопросом
    function course_complete_from_step_with_question(modalHTML) {


        // Добавляем полученный modal в подготовленное место в шаблоне
        $('.modal_place').html(modalHTML)

        // Открываем modal через bootstrap'овский метод modal
        $('#courseCompleteModal').modal('show')
        

    }

    $('#testModalButton').click(function (e) { 
        e.preventDefault();
        $('#courseCompleteModal').modal("show")
        $('#offcanvasPointList').offcanvas("hide")
    });

    var currentCheck;
    var currentChecks = [];


    // Если шаг не имеет вопроса, то отправляем в ajax_make_step_is_completed и вносим шаг в 
    // progress.completed_steps, попутно проверяя не завершился ли курс?
    if (stepHasQuestions === 'false') {
        $.ajax({
            type: "POST",
            url: urlForMakeStepIsCompleted,
            headers: {
                'X-CSRFToken': csrfToken,
            },
            data: {
                'progress_pk': progressPk,
                'total_steps_in_course': total_steps_in_course
            },
            dataType: "json",
            success: function (response) {
                // Если шаг завершен
                if (response.status === "step_is_completed") {
                    console.log('step_is_completed')
                    // Пока ничего не делаем

                    // Если завершился курс на этом шаге
                } else if (response.status === "course_is_competed") {
                    console.log('Курс завершен, это последний шаг')
                    // При получении ответа приходит так же html модального окна
                    var modalHtml = response.modal_for_course_completed

                    // Вызываем course_complete_from_simple_step, которая рендерит модальное окно,
                    // но не вызывает его, а рендерит так же кнопку "Завершить курс", вызывающую модальное окно
                    course_complete_from_simple_step(modalHtml = modalHtml)
                }
            }
        });

        // Если шаг имеет вопрос, то получаем информацию из поля 
    } else if (stepHasQuestions === 'true') {

        // Проверяем, имеется один ответ на вопрос или несколько?
        if (question_has_many_correct_answers === 'False') {

            // Если у вопроса один правильный ответ.
            // Отслеживаем нажатие чекбоксов. При выборе другого, снимаем отметку с другого нажатого и активируем кнопку отправить.
            $('input[name="answer"]').change(function () {
                currentCheck = $(this)

                // Снимаем отметку со всех чекбоксов, кроме текущего
                $('input[name="answer"]').not(this).prop('checked', false);

                // Проверяем, есть ли хотя бы один отмеченный чекбокс
                var anyChecked = $('input[name="answer"]:checked').length > 0;

                // Активируем или деактивируем кнопку отправки
                $('#sendAnswerButton').prop('disabled', !anyChecked)
            });

            // Отслеживаем отправку submit
            $('#formForQuestion').submit(function (e) {
                e.preventDefault();

                // сохраняем форму (данные):
                var formData = $(this).serialize();
                // сохраняем pk вопроса для проверки ответов во view
                var questionPk = $(this).attr('question-pk');

                $.ajax({
                    type: "POST",
                    url: ajax_check_answer_for_question, // url из шаблона
                    data: formData + '&question_pk=' + questionPk + '&progress_pk=' + progressPk + '&total_steps_in_course=' + total_steps_in_course,
                    dataType: "json",
                    success: function (response) {

                        // Ответ correct_answer приходит тогда, ответ правильный, но курс не завершен
                        if (response.status === "correct_answer") {
                            //Сообщение об успешном ответе.
                            $('.user-answer-status').removeClass('d-none');
                            $('.user-answer-status').attr("style", "color: green");
                            $('.user-answer-status').html("Это правильный ответ.");
                            $('#sendAnswerButton').attr("disabled", true);
                            $('input[name="answer"]').not(currentCheck).attr("disabled", true);
                            $('input[name="answer"]').not(currentCheck).next('span').addClass("text-muted");
                            currentCheck.next('span').attr('style', 'color: green');
                            currentCheck.next('span').after(`<span style="content: url('/static/education_platform/common_icons/list-check-mark.svg');
                                        width: 15px; position: absolute; margin: 5px 0px 0px 5px;">
                                        </span>`)


                            // Если ответ неправильный
                        } else if (response.status === "incorrect_answer") {
                            $('.user-answer-status').removeClass('d-none');
                            $('.user-answer-status').attr("style", "color: red")
                            $('.user-answer-status').html("Неверно. Попробуйте еще раз.");
                            currentCheck.prop("checked", false)

                            // Если ответ правильный и курс завершен на этом шаге.   
                        } else if (response.status === "course_is_competed") {
                            $('.user-answer-status').removeClass('d-none');
                            $('.user-answer-status').attr("style", "color: green");
                            $('.user-answer-status').html("Это правильный ответ.");
                            $('#sendAnswerButton').attr("disabled", true);
                            $('input[name="answer"]').not(currentCheck).attr("disabled", true);
                            $('input[name="answer"]').not(currentCheck).next('span').addClass("text-muted");
                            currentCheck.next('span').attr('style', 'color: green');
                            currentCheck.next('span').after(`<span style="content: url('/static/education_platform/common_icons/list-check-mark.svg');
                                        width: 15px; position: absolute; margin: 5px 0px 0px 5px;">
                                        </span>`)

                            // При получении ответа приходит так же html модального окна
                            var modalHtml = response.modal_for_course_completed

                            // Вызываем функцию course_complete_from_step_with_question, которая 
                            // рендерит и вызывает модальное окно
                            course_complete_from_step_with_question(modalHTML = modalHtml)

                        }
                    }
                });
            });
        } //Тут заканчивается логика с одним правильным ответом у вопроса

        // Если у вопроса несколько правильных ответов:
        else if (question_has_many_correct_answers === 'True') {
            // отслеживаем нажатие чекбоксов
            $('input[name="answer"]').change(function (e) {

                // Добавляем выбранные check в список currentChecks
                currentChecks.push($(this))

                // если нажат хотя бы один чекбокс
                var anyChecked = $('input[name="answer"]:checked').length > 0;

                //то делаем кнопку отправить доступной
                $('#sendAnswerButton').prop('disabled', !anyChecked)

            });

            // Отслеживаем отправку submit
            $('#formForQuestion').submit(function (e) {
                e.preventDefault();
                $('.answer-loader').removeClass("d-none")

                // Сохраняем форму
                var formData = $(this)

                // сохраняем pk вопроса
                var questionPk = formData.attr('question-pk');


                // Отправляем данные из формы в ajax_check_answer_for_question (view) попутно проверяя не завершился ли курс
                $.ajax({
                    type: "POST",
                    url: ajax_check_answer_for_question,
                    data: formData.serialize() + '&question_pk=' + questionPk + '&progress_pk=' + progressPk + '&total_steps_in_course=' + total_steps_in_course,
                    dataType: "json",
                    success: function (response) {

                        // Ответ correct_answers, если ответы правильные, но курс не завершен
                        if (response.status === "correct_answers") {
                            $('.answer-loader').addClass('d-none')
                            $('.user-answer-status').removeClass('d-none');
                            $('.user-answer-status').attr("style", "color: green");
                            $('.user-answer-status').html("Вы ответили правильно.");
                            $('input[name="answer"]').attr("disabled", true)

                            $('input[name="answer"]').next('span').addClass("text-muted")
                            $('#sendAnswerButton').attr("disabled", true);

                            $.each(currentChecks, function (indexInArray, valueOfElement) {
                                valueOfElement.next('span').removeClass("text-muted")
                                valueOfElement.next('span').after(`<span style="content: url('/static/education_platform/common_icons/list-check-mark.svg');
                                        width: 15px; position: absolute; margin: 5px 0px 0px 5px;">
                                        </span>`)
                            });



                            // Если ответы неправильные
                        } else if (response.status === "incorrect_answers") {
                            $('.answer-loader').addClass('d-none')
                            $('input[name="answer"]').prop('checked', false)
                            $('.user-answer-status').removeClass('d-none');
                            $('.user-answer-status').attr("style", "color: red")
                            $('.user-answer-status').html("Неверно. Попробуйте еще раз.");

                            // Если ответы правильные и курс завершен на этом шаге
                        } else if (response.status === "course_is_competed") {
                            // При получении ответа приходит так же html модального окна
                            var modalHtml = response.modal_for_course_completed
                            course_complete_from_step_with_question(modalHTML = modalHtml)
                        }
                    }
                });

            });
        }
    }

    // Корректировка контейнера с навигационными кнопками, если контента не хватает на всю высоту экрана
    var footerHeight = $('.footer').height() // Высота футера
    var contentHeight = $('.step_main_content-wrapper').height() + 56 + footerHeight //Высота всего контента за минусом nav и footer
    var screenHeight = $(window).height(); //Высота экрана

    var emptySpace = screenHeight - contentHeight // Пустое место на экране

    if (emptySpace > 0) {
        var lastElementHeight = $('.step_navigation_buttons-wrapper').height()
        $('.step_navigation_buttons-wrapper').css("height", lastElementHeight + emptySpace)
    } else {
        // Пока ничего не делаем
    }


    // Корректировка работы навигационных ссылок step_nav_square (ссылка срабатывает даже при наведении на <div> а не на <a>)
    $(".step_nav_square").click(function (e) {
        e.preventDefault();
        // Находим ссылку внутри текущего div
        var link = $(this).find('.step_nav_link').attr("href");
        window.location.href = link
    });




});


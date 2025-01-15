$(document).ready(function () {
    // Фиксируем высоту navbar для дальнейшей навигации
    var navbarHeight = $('.navbar').outerHeight();

    //Функция для проверки длины содержимого полей редакторов, исключая теги
    function getTextLengthWithoutTags(element) {
        return (element.textContent.trim()).length;
    }

    // Отправка нового комментария для шага
    // Отслеживание нажатия кнопки оставить комментарий
    $('.add_new_comment_button').click(function (e) {
        e.preventDefault();

        var current_button = $(this)

        // Скрываем кнопку
        current_button.fadeOut(200);

        // Сохраняем объект формы
        var currentFormWrapper = $('.form-for-new_comment_wrapper');

        // Делаем форму для нового комментария видимой
        if (currentFormWrapper.hasClass('form-for-new_comment_wrapper__hide')) {
            currentFormWrapper.removeClass('form-for-new_comment_wrapper__hide');
            currentFormWrapper.addClass("form-for-new_comment_wrapper__show");
        }

        // Инициализируем editor (quill)
        // В этот момент создается элемент с классом toolbar, содержащий кнопки управления toolbar'ом. 
        // Он будет размещен перед #editor-new_comment
        // Так же у #editor-new_comment добавляются классы ql-container и ql-snow
        var editorContainer = $('#editor-new_comment');
        var quill = new Quill(editorContainer.get(0), {
            theme: 'snow',
            modules: {
                toolbar: [
                    [{ 'header': [1, 2, false] }],
                    ['bold', 'italic', 'underline', 'strike'],
                    ['link'],
                ]
            }
        });


        // Перемещаем пользователя на место открывшейся формы
        $('html, body').animate({
            scrollTop: currentFormWrapper.offset().top - navbarHeight - 2
        }, 300);

        // Устанавливаем фокус на редакторе комментария
        quill.focus();


        // Проверяем количество символов в editorContainer (это поле от quill, которое далее будет передано в инпут для дальнейшей обработки)
        // Включаем кнопку send_new_comment_button, если количество символов больше 2, то включаем кнопку send_new_comment_button
        var keyupHandler = function (e) {
            var charsCountInEditor = getTextLengthWithoutTags(editorContainer.get(0));
            if (charsCountInEditor > 2) {
                $('.send_new_comment_button').attr('disabled', false);
            } else {
                $('.send_new_comment_button').attr('disabled', true);
            }
        };

        editorContainer.on('keyup', keyupHandler);

        // Перед отправкой, ожидаем возможное нажатие отмены (cancel_send_new_comment_button)
        $('.cancel_send_new_comment_button').click(function (e) {
            e.preventDefault();
            currentFormWrapper.removeClass('form-for-new_comment_wrapper__show');
            currentFormWrapper.addClass("form-for-new_comment_wrapper__hide");
            var toolbarElement = currentFormWrapper.find('.ql-toolbar');
            toolbarElement.remove();

            // Удаляем классы ql-container и ql-snow у editorContainer
            editorContainer.removeClass("ql-container").removeClass("ql-snow");
            editorContainer.empty();

            current_button.fadeIn(200);

            // Удаляем обработчик события keyup
            editorContainer.off('keyup', keyupHandler);
            quill.setText('');

            // Отключаем обработчик событий отслеживания отправки формы
            $('.form_for_new_comment').off('submit');

            return;
        });

        // Отслеживаем отправку формы с новым комментарием
        $('.form_for_new_comment').submit(function (e) {
            e.preventDefault();

            // Получаем данные из Quill
            var commentText = quill.root.innerHTML;

            // Дополнительная проверка, не отправлена ли все-таки пустая строка
            var isEmpty = getTextLengthWithoutTags(editorContainer.get(0)) > 2;
            if (!isEmpty) {
                alert("Слишком короткий текст комментария.");
                return;
            }

            // Помещаем данные в инпут формы
            $(this).find('input[name="comment_text"]').val(commentText);

            // Отправляем запрос POST
            $.ajax({
                type: "POST",
                url: $(this).attr('action'),
                data: $(this).serialize(),
                dataType: "json",
                success: function (response) {
                    if (response.status === "success") {
                        // Удаляем wrapper формы из которой отправляли
                        currentFormWrapper.remove();

                        // В ответе получаем new_comment_html с html новго комментария
                        // Так же получаем его новый ID чтобы сразу его найти
                        var newCommentId = response.new_comment_id;
                        var newCommentHtml = response.new_comment_html;

                        // Вставляем новый комментарий в начало списка комментариев
                        $('.all_comments-wrapper').prepend(newCommentHtml)

                        // Находим вставленный элемент, он приходит со свойством display: none
                        var newComment = $(`.comment_item[id=${newCommentId}]`)

                        // Показываем элемент и перемещаемся к нему
                        /*                         $('html, body').animate({
                                                    scrollTop: newComment.offset().top
                                                }, 200); */
                        newComment.fadeIn(350)
                        


                    }
                }
            });
        });
    });



    // Отправка ответа на комментарий
    $('.comments-answer-button').click(function (e) {

        var current_answer_button = $(this);
        e.preventDefault();
        // Скрываем кнопку
        current_answer_button.fadeOut(200);


        var commentId = $(this).attr('id')

        // Ищем нужный комментарий под которым нажата кнопка ответить
        var currentFormWrapper = $(`.form-for-answer_comment_wrapper[id=${commentId}]`);

        //Делаем его форму комментария видимой
        if (currentFormWrapper.hasClass("form-for-answer_comment_wrapper__hide")) {
            currentFormWrapper.removeClass("form-for-answer_comment_wrapper__hide");
            currentFormWrapper.addClass("form-for-answer_comment_wrapper__show");
        }

        // Определяем заранее форму с которой работаем, чтобы отключить обработчик события, в случае отмены
        var currentForm = $(currentFormWrapper).find(`.form_for_answer_comment[id=${commentId}]`)




        // Инициируем toolbar
        var editorContainer = currentFormWrapper.find(`#editor-${commentId}`);
        var quill = new Quill(editorContainer.get(0), {
            theme: 'snow',
            modules: {
                toolbar: [
                    [{ 'header': [1, 2, false] }],
                    ['bold', 'italic', 'underline', 'strike'],
                    ['link'],
 
                ]
            }
        });

        // Добавляем в quill автора родительского комментария, на который пишем ответ
        quill.setContents([
            { insert: '@' + currentForm.attr("author") + ",", attributes: { bold: true } },
            { insert: " ", attributes: { bold: false } }
        ]);

        // Длина строки автора, которому отвечаем, для дальнейшего использования
        var lengthAuthorString = currentForm.attr("author").length;

        // Перемещаем каретку в положение после имени автора
        quill.setSelection(lengthAuthorString + 3, lengthAuthorString + 3);

        // Перемещаем пользователя на место открывшейся формы
        $('html, body').animate({
            scrollTop: currentFormWrapper.offset().top - navbarHeight - 5
        }, 300);

        // Устанавливаем фокус на редакторе комментария
        quill.focus();

        // Проверяем количество символов в editorContainer (это поле от quill, которое далее будет передано в инпут для дальнейшей обработки)
        // Включаем кнопку send_new_comment_button, если количество символов больше 2, то включааем кнопку send_new_comment_button
        editorContainer.keyup(function (e) {
            var charsCountInEditor = getTextLengthWithoutTags(editorContainer.get(0));
            if (charsCountInEditor > 2) {
                $(`.send_answer_for_comment_button[id=${commentId}]`).attr('disabled', false);
            } else {
                $(`.send_answer_for_comment_button[id=${commentId}]`).attr('disabled', true);
            }
        });

        // Перед отправкой ожидаем действие отмены отправки.
        // Отслеживаем нажатие кнопки отмена
        $(`.answer_for_comment_cancel_button-${commentId}`).click(function (e) {
            e.preventDefault();
            currentFormWrapper.removeClass('form-for-answer_comment_wrapper__show');
            currentFormWrapper.addClass("form-for-answer_comment_wrapper__hide");
            var toolbarElement = currentFormWrapper.find('.ql-toolbar');
            toolbarElement.remove();
            quill.setText('');
            current_answer_button.fadeIn(200);

            // Удаляем классы ql-container и ql-snow у editorContainer
            editorContainer.removeClass("ql-container").removeClass("ql-snow");

            // Очищаем содержимое котейнера
            editorContainer.empty();

            editorContainer.off('keyup');
            currentForm.off('submit') // Удаляем обработчик события submit
            return;

        });



        // Отслеживаем отправку формы
        currentForm.submit(function (e) {
            e.preventDefault();
            // Извлекаем данные из editor'а и помещаем в форму


            // Получаем данные из Quill
            var commentText = quill.root.innerHTML;


            // Дополнительная проверка, не отправлена ли все-таки пустая строка
            var isEmpty = getTextLengthWithoutTags(editorContainer.get(0)) > 2;
            if (!isEmpty) {
                alert("Cлишком короткий текст комментария.");
                return;
            }


            // Помещаем в нужный инпут
            currentForm.find('input[name="comment_text"]').val(commentText);

            $.ajax({
                type: "POST",
                url: currentForm.attr("action"),
                data: currentForm.serialize(),
                dataType: "json",
                success: function (response) {
                    if (response.status === "success") {
                        // Удаляем wrapper формы из которой отправляли
                        currentFormWrapper.remove();

                        // В ответе есть html созданного ответа new_answer_html
                        var newAnswerHtml = response.new_answer_html

                        // Так же в ответе есть comment_pk список ответов которого будем искать
                        var currentCommentPk = response.comment_pk

                        // В ответе есть new_answer_pk для поиска нового ответа по id
                        var newAnwperId = response.new_answer_pk

                        // Находим список ответов к которому необходимо добавить комментарий
                        var currentAnswersList = $(`.all_answers-wrapper-for-comment-${currentCommentPk}`)

                        // Добавляем в начало списка новый ответ
                        currentAnswersList.prepend(newAnswerHtml)

                        // Находим новый ответ
                        var newCommentObj = $(`.comment_item[id=${newAnwperId}]`)
                        newCommentObj.fadeIn(350);
                        currentAnswersList.fadeIn(350);


                    }
                }
            });


        });
    });




    // Запрос загрузки ответов к комментариям
    $('.comments-answers_list-button').click(function (e) {
        e.preventDefault();

        // Убираем кнопку "Посмотреть ответы"
        $(this).fadeOut(100);

        var current_button = $(this);
        var current_coment_id = current_button.attr("id")
        var current_answers_place = $(`.all_answers-wrapper-for-comment-${current_coment_id}`)

        // Определяем кнопку закрывания списка ответов и делаем ее видимой
        var current_close_button = $(`.comments-answers_list-close-button[id=${current_coment_id}]`)
        setTimeout(function() {
            current_close_button.fadeIn(200);
        }, 150)


        // Отслеживаем закрывание списка ответов
        current_close_button.click(function (e) { 
            e.preventDefault();
            current_answers_place.fadeOut(200);
            setTimeout(function() {
                current_answers_place.empty();
            }, 200)

            
            current_close_button.fadeOut(100);
            setTimeout(function() {
                current_button.fadeIn(200);
            }, 150)

        });
        



        $.ajax({
            type: "GET",
            url: current_button.attr('get_answers_list_url'),
            dataType: "json",
            success: function (response) {
                if (response.status === "success") {
                    var answerListHtml = response.answers_html

                    // вставить в current_answers_place список answerListHtml
                    current_answers_place.html(answerListHtml)
                    current_answers_place.fadeIn(200)


                    // Отправка отета на ответ
                    // Отслеживаем нажатие кнопки
                    $('.comments-answer_for_answer-button').click(function (e) {
                        e.preventDefault();

                        var current_answer_button = $(this);
                        e.preventDefault();
                        // Скрываем кнопку
                        current_answer_button.fadeOut(200);

                        var answerId = current_answer_button.attr("id")

                        // Ищем нужный ответ под которым нажата кнопка ответить
                        var currentFormWrapper = $(`.form-for-answer_for_answer_wrapper[id=${answerId}]`);

                        //Делаем его форму комментария видимой
                        if (currentFormWrapper.hasClass("form-for-answer_for_answer_wrapper__hide")) {
                            currentFormWrapper.removeClass("form-for-answer_for_answer_wrapper__hide");
                            currentFormWrapper.addClass("form-for-answer_for_answer_wrapper__show");
                        }

                        // Определим текущую форму
                        var currentForm = $(currentFormWrapper).find(`.form_for_answer_comment`)

                        // Длина строки автора, которому отвечаем, для дальнейшего использования
                        var lengthAuthorString = currentForm.attr("author").length;

                        // Инициируем toolbar
                        var editorContainer = currentFormWrapper.find(`#editor-${answerId}`);
                        var quill = new Quill(editorContainer.get(0), {
                            theme: 'snow',
                            modules: {
                                toolbar: [
                                    [{ 'header': [1, 2, false] }],
                                    ['bold', 'italic', 'underline', 'strike'],
                                    ['link'],
                                ]
                            }
                        });

                        // Добавляем в quill автора родительского комментария, на который пишем ответ
                        quill.setContents([
                            { insert: '@' + currentForm.attr("author") + ",", attributes: { bold: true } },
                            { insert: " ", attributes: { bold: false } }
                        ]);

                        quill.setSelection(lengthAuthorString + 3, lengthAuthorString + 3);


                        // Перемещаем пользователя на место открывшейся формы
                        $('html, body').animate({
                            scrollTop: currentFormWrapper.offset().top - navbarHeight - 2
                        }, 500);

                        // Устанавливаем фокус на редакторе комментария
                        quill.focus();


                        // Проверяем количество символов в editorContainer (это поле от quill, которое далее будет передано в инпут для дальнейшей обработки)
                        // Включаем кнопку send_new_comment_button, если количество символов больше 2, то включааем кнопку send_new_comment_button
                        editorContainer.keyup(function (e) {
                            var charsCountInEditor = getTextLengthWithoutTags(editorContainer.get(0));
                            var lengthAuthorString = currentForm.attr("author").length;
                            if (charsCountInEditor > 3 + lengthAuthorString) {
                                $(`.send_answer_answer_for_comment_button[id=${answerId}]`).attr('disabled', false);
                            } else {
                                $(`.send_answer_answer_for_comment_button[id=${answerId}]`).attr('disabled', true);
                            }
                        });


                        // Перед отправкой (пока форма открыта) ожидаем действие отмены отправки.
                        // Отслеживаем нажатие кнопки отмена
                        $(`.answer_for_comment_cancel_button-${answerId}`).click(function (e) {
                            e.preventDefault();
                            currentFormWrapper.removeClass('form-for-answer_for_answer_wrapper__show');
                            currentFormWrapper.addClass("form-for-answer_for_answer_wrapper__hide");
                            var toolbarElement = currentFormWrapper.find('.ql-toolbar');
                            toolbarElement.remove();
                            quill.setText('');
                            current_answer_button.fadeIn(200);

                            // Удаляем классы ql-container и ql-snow у editorContainer
                            editorContainer.removeClass("ql-container").removeClass("ql-snow");

                            // Очищаем содержимое котейнера
                            editorContainer.empty();

                            editorContainer.off('keyup');
                            currentForm.off('submit') // Удаляем обработчик события submit
                            return;

                        });

                        $(currentForm).submit(function (e) {
                            e.preventDefault();
                            // Дополнительная проверка, не отправлена ли все-таки пустая строка
                            var isEmpty = getTextLengthWithoutTags(editorContainer.get(0)) > 2;
                            if (!isEmpty) {
                                alert("Cлишком короткий текст комментария.");

                                editorContainer.off('keyup');
                                currentForm.off('submit') // Удаляем обработчик события submit

                                return;
                            }

                            // Получаем данные из Quill
                            var commentText = quill.root.innerHTML;


                            // Помещаем в нужный инпут
                            currentForm.find('input[name="comment_text"]').val(commentText);


                            $.ajax({
                                type: "POST",
                                url: currentForm.attr("action"),
                                data: currentForm.serialize(),
                                dataType: "json",
                                success: function (response) {
                                    if (response.status === "success") {
                                         // Удаляем wrapper формы из которой отправляли
                                        currentFormWrapper.remove();

                                        // В ответе есть html созданного ответа new_answer_html
                                        var newAnswerHtml = response.new_answer_html

                                        // Так же в ответе есть comment_pk список ответов которого будем искать
                                        var currentCommentPk = response.comment_pk

                                        // В ответе есть new_answer_pk для поиска нового ответа по id
                                        var newAnwperId = response.new_answer_pk

                                        // Находим список ответов к которому необходимо добавить комментарий
                                        var currentAnswersList = $(`.all_answers-wrapper-for-comment-${current_coment_id}`)

                                        // Добавляем в начало списка новый ответ
                                        currentAnswersList.append(newAnswerHtml)

                                        // Находим новый ответ
                                        var newCommentObj = $(`.comment_item[id=${newAnwperId}]`)
                                        newCommentObj.fadeIn(350);


                                    }
                                }
                            });
                        });
                    });

                }
            }
        });


    });




});
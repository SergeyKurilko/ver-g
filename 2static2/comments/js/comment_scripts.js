$(document).ready(function () {
    //Создание нового комментария через ajax и back
    $('#addNewCommentForm').submit(function (e) { 
        e.preventDefault();
        var addNewCommentForm = $(this)
        $.ajax({
            type: addNewCommentForm.attr("method"),
            url: addNewCommentForm.attr("action"),
            data: addNewCommentForm.serialize(),
            success: function (response) {
                if (response.status === 'success') {
                    $('#addNewCommentCollapse').fadeOut(1000, function() {

                        //добавление нового комментария на страницу
                        var NewCommentHtml = `
                        <div class="container mt-3" id="OneCommentContainer">
                        <div class="mt-3">
                        <span style="font-weight: 600;">${$('#id_author').val()}</span> | <span style="font-size: 0.8em;">${new Date().toLocaleString()}</span>
                        <p style="margin-bottom: 0 !important">${$(`#id_text`).val()}</p>
                        <p style="margin-bottom: 0 !important; color: #FF4A00 !important">
                        это ваш комментарий, ${$('#id_author').val()}, на него могут ответить другие пользователи
                        </p>

                        `
                        $('#noCommentsForArticle').remove();
                        $('#allCommentsContainer').prepend(NewCommentHtml);

                        var windowHeight = $(window).height()
                        $('html, body').animate({
                            scrollTop: $('#allCommentsContainer').offset().top - (windowHeight / 2)
                        }, 300);

                        //Запуск toast
                        var successToastElem = $('#liveToast');
                        var toast = new bootstrap.Toast(successToastElem, {
                            delay: 3000
                        });
                        console.log('Запуск toast')
                        toast.show();
                        console.log('toast запущен')
                        //TODO: определить, что делать, если этот же пользователь пойдет отвечать на коммент.
                    });
                } else if (response.status === 'error') {
                    $('#textForAlertsModal').text(response.message)
                    $('#commentsAlertModal').modal('show')
                }
            }
        });
    });
    console.log("Waiting submit")

    //Отслеживание формы добавления ответа к комментарию
    //$('.addAnswerForCommentForms').submit(function (e) { 
        $('#allCommentsContainer').on('submit', '.addAnswerForCommentForms', function (e) {
        e.preventDefault();
        var addAnswerForCommentForm = $(this)
        $.ajax({
            type: addAnswerForCommentForm.attr("method"),
            url: addAnswerForCommentForm.attr("action"),
            data: addAnswerForCommentForm.serialize(),
            success: function (response) {
                if (response.status === 'success') {
                    $('#dangerAlert').addClass('d-none');
                    var parentId = response.parent
                    var addAnswerCollapse = `#addAnswerCollapse${parentId}`
                    $(addAnswerCollapse).fadeOut(1000, function() {
                        $('#dangerAlert').remove();


                        //извлекаем данные из формы для дальнейшего рендера
                        var author = $(`#addAnswerForCommentForm${parentId} #id_author`).val()
                        var text = $(`#addAnswerForCommentForm${parentId} #id_text`).val()
                        console.log("Четвертая точка")

                        //Если это не первый ответ, то добавляем его в начало списка ответов этого комментария 
                        if (response.it_first_answer === false) {
                            console.log("Пятая точка")
                            var newAnswerHtml = `
                            <div class="mt-3 answer_item">
                            <span style="font-weight: 600;">${author}</span> | <span style="font-size: 0.8em;">${new Date().toLocaleString()}</span>
                            <p style="margin-bottom: 0 !important">
                            ${text}
                            </p>
                            </div>
                            `       
                            $(`#answersForComment${parentId}`).prepend(newAnswerHtml)    
                        } 
                        //Если ответ является первым у этого комментария, то создаем список ответов и помещаем туда ответ.
                        else if (response.it_first_answer) {
                            var newAnswerHtml = `
                                <div class="" id="answersForComment${parentId}" style="">
                                <div class="mt-3 answer_item">
                                <span style="font-weight: 600;">${author}</span> | <span style="font-size: 0.8em;">${new Date().toLocaleString()}</span>
                                <p style="margin-bottom: 0 !important">
                                ${text}
                                </p>
                                </div>
                                </div>
                            `
                            $(`#OneCommentContainer${parentId}`).append(newAnswerHtml)
                            $(`#buttonForAnswer${parentId}`).after(`
                                <a href="" class="answersForCommentButton" data-bs-toggle="collapse" data-bs-target="#answersForComment${parentId}">
                                ответы (1)
                                </a>&nbsp;&nbsp;`)
                        }
                                    
                        
                        var windowHeight = $(window).height()
                        $('html, body').animate({
                            scrollTop: $(`#answersForComment${parentId}`).offset().top - (windowHeight / 2)
                        }, 300);
                        
                        //Запуск toast
                        var successToastElem = $('#liveToast');
                        var toast = new bootstrap.Toast(successToastElem, {
                            delay: 3000
                        });
                        toast.show();
                    })
                } else if (response.status === 'error') {
                    $('#textForAlertsModal').text(response.message)
                    $('#commentsAlertModal').modal('show')
                }
            }
        });
    });

    //Отслеживаем нажатие кнопки подгрузки комментариев. 
    $('#load-more-comments').click(function (e) { 
        e.preventDefault();

        //Для url используем переменную requestPath, созданную в шаблоне
        //Определим переменную offset, чтобы затем передать ее в вьюху
        //offset нужен для создания слайса из комментариев, его отправной точки
        //Получаем ее из элемента #load-more-comments и его атрибута data-offset="3"
        var commentOffset = $(this).data('offset')
        $.ajax({
            type: "get",
            url: requestPath,
            data: {
                'offset': commentOffset
            },
            dataType: "json",
            success: function (response) {

                //из вьюхи получаем список словарей с ключами author, text, published, comment.id, article_id, csrf_token_for_answer_form
                //определим этот список в переменную comments
                var comments = response.comments;
                console.log(comments.length)

                if (comments.length === 0) {
                    console.log('Пусто!')
                    $('#load-more-comments').html('<span>Больше нет комментариев</span>')
                }

                //Перебираем элементы (словари) и рендерим полученные комментарии:
                comments.forEach(comment => {
                    var moreCommentHtml = `
                        <div class="container mt-3" id="OneCommentContainer${comment.id}">
                        <div class="mt-3">
                        <span style="font-weight: 600;">${comment.author}</span> | <span style="font-size: 0.8em;">${comment.published}</span>
                        <p style="margin-bottom: 0 !important">
                        ${comment.text}
                        </p>
                        <a class="buttonForAnswer" id="buttonForAnswer${comment.id}" href="#" data-bs-toggle="collapse" data-bs-target="#addAnswerCollapse${comment.id}">
                        Ответить</a>&nbsp&nbsp


                        <div class="collapse m-1 p-1" id="addAnswerCollapse${comment.id}">

                        <div class="alert alert-success d-none" role="alert" id="successAlert">
                        </div>

                        <div class="alert alert-danger d-none" role="alert" id="dangerAlert">
                        </div>

                        <form class="addAnswerForCommentForms p-2" id="addAnswerForCommentForm${comment.id}" action="/comments/add_answer_for_comment/${comment.article_id}/${comment.id}/" method="post">
                        <input type="hidden" name="csrfmiddlewaretoken" value="${comment.csrf_token_for_answer_form}">
                        <h5>Введите ваше имя и текст сообщения</h5>
                        <p><input type="text" name="author" class="form-control w-50" placeholder="Имя" maxlength="50" required="" id="id_author"></p>
                        <p><textarea name="text" cols="40" rows="10" class="form-control" placeholder="Текст сообщения" required="" id="id_text"></textarea></p>
                        <button class="btn btn-warning mt-1 orangeButtonForSendComments" type="submit">Отправить</button>
                        </form>
                        </div>
                    `;
                    if (comment.answers_count > 0) {
                        moreCommentHtml += `
                        <a href=""
                        class="answersForCommentButton"
                        data-bs-toggle="collapse"
                        data-bs-target="#answersForComment${comment.id}">
                        ответы (${comment.answers_count})
                        </a>
                        <div id="answersForComment${comment.id}" class="collapse">
                    `;
                    comment.answers.forEach(answer => {
                        console.log('answer')
                        moreCommentHtml += `
                        <div class="mt-3 answer_item">
                        <span style="font-weight: 600;">${answer.answer_author}</span> | <span style="font-size: 0.8em;">${answer.answer_published}</span>
                        <p style="margin-bottom: 0 !important">
                        ${answer.answer_text}
                        </p>
                        </div>
                    `;});
                    moreCommentHtml += `
                    </div>
                    </div>
                    `
                    }

                    $('#allCommentsContainer').append(moreCommentHtml);         
                });

                //Увеличим data-offset у кнопки #load-more-comments на 3, чтобы при следующем запросе получить новый слайс
                $('#load-more-comments').data('offset', commentOffset + 3)
                
            }
        });
    });

    $(`#addNewCommentCollapseButton`).click(function (e) {
        if ($(this).hasClass('addNewCommentCollapseButtonClass')) {
            $(this).removeClass('addNewCommentCollapseButtonClass');
            $(this).addClass('addNewCommentCollapseButtonClassPushed')
        } else if ($(this).hasClass('addNewCommentCollapseButtonClassPushed')) {
            $(this).addClass('addNewCommentCollapseButtonClass')
            $(this).removeClass('addNewCommentCollapseButtonClassPushed')
        }    
    });

    //Article Rate
    //Отслеживаем нажатие на кнопку с оценкой
    $('.article_rate_link').click(function (e) { 
        e.preventDefault();

        //у элемента есть атрибут data-rate, оттуда извлекаем знаеие rate
        rate = $(this).data('rate')

        //Переменные this_article_id, url_for_rate и token_for_rate передаются из шаблона article_detail
        //ajax
        console.log(token_for_rate)
        console.log(rate)
        $.ajax({
            type: "POST",
            url: url_for_rate,
            data: {
                'rate': rate,
                'csrfmiddlewaretoken': token_for_rate
            },
            success: function (response) {
                if (response.status === "success") {
                    $('.article_rate_list_container').remove()
                    $('.rate_the_article_title').html('<div class="rate_the_article_title ms-4 me-4">Спасибо за оценку!</div>')
                }
            }
        });

    });

});




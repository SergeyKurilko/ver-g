from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.conf import settings

from education_platform.models import StepForPoint, CommentForStep
from education_platform.tasks import send_telegram_step_comment


def add_answer_for_comment_for_step_view(request, comment_pk):
    """
    Принимает ajax с формой текста ответа на комментарий pk комментария.
    Создает объект CommentForStep, возвращает Json
    """
    if request.method == "POST":
        # Извлекаем текст ответа на комментарий
        answer_text = request.POST.get("comment_text")

        if answer_text:
            # Комментарий, к которому добавляется ответ
            current_comment = get_object_or_404(CommentForStep, pk=comment_pk)

            # Шаг
            current_step = current_comment.step

            # Создаем новый объект CommentForStep
            new_answer = CommentForStep.objects.create(
                author = request.user,
                step = current_step,
                text = answer_text,
                parent = current_comment
            )

            new_comment_author_avatar_url = False

            if request.user.student.avatar:
                new_comment_author_avatar_url = request.user.student.avatar.url

            new_answer_context = {
                "new_answer_pk": new_answer.pk,
                "new_answer_author_avatar_url": new_comment_author_avatar_url,
                "new_answer_author": f"{request.user.first_name} {request.user.last_name}",
                "new_answer_date": new_answer.published,
                "new_answer_text": new_answer.text,
            }

            send_telegram_step_comment.delay(comment={
                                                 "comment_pk": new_answer.pk,
                                                 "current_step_pk": current_step.pk,
                                                 "author_email": request.user.email,
                                                 "date": new_answer.published,
                                                 "text": new_answer.text
                                             })


            return JsonResponse({
                "status": "success",
                "comment_pk": current_comment.pk,
                "new_answer_pk": new_answer.pk,
                "new_answer_html": render_to_string("education_platform/incl/new_answer_for_paste.html",
                                               context=new_answer_context)
            })
    else:
        return redirect("education_platform:home")


def add_new_comment_for_step_ajax_view(request, step_pk):
    if request.method == "POST":
        current_step = get_object_or_404(StepForPoint, pk=step_pk)
        comment_text = request.POST.get("comment_text")
        if comment_text and len(comment_text) > 0:
            new_comment = CommentForStep.objects.create(
                author = request.user,
                step = current_step,
                text=comment_text,
            )

            new_comment_author_avatar_url = False

            if request.user.student.avatar:
                new_comment_author_avatar_url = request.user.student.avatar.url

            new_comment_context = {
                "new_comment_pk" : new_comment.pk,
                "new_comment_date": new_comment.published,
                "new_comment_text": new_comment.text,
                "new_comment_author": f"{request.user.first_name} {request.user.last_name}",
                "new_comment_author_avatar_url": new_comment_author_avatar_url
            }

            send_telegram_step_comment.delay(comment={
                                                 "comment_pk": new_comment.pk,
                                                 "current_step_pk": current_step.pk,
                                                 "author_email": request.user.email,
                                                 "date": new_comment.published,
                                                 "text": new_comment.text
                                             })

            return JsonResponse({
                "status": "success",
                "new_comment_id": new_comment.pk,
                "new_comment_html" :
                    render_to_string('education_platform/incl/new_comment_for_paste.html',
                                     context=new_comment_context)
            })
        else:
            return JsonResponse({
                "status": "new_comment_form_error",
                "error": "Поле не может быть пустим"
            })

    else:
        return redirect("education_platform:home")


def get_answers_for_comment(request, comment_pk):
    answers = CommentForStep.objects.filter(
        parent_id=comment_pk).order_by('published')

    answer_list_context = {
        "answers": answers,
    }
    return JsonResponse({
        "status": "success",
        "answers_html": render_to_string(
            'education_platform/incl/answer_list_for_comment.html',
            context=answer_list_context,
            request=request
        )
    })
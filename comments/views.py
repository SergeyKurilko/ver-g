from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from blog.models import Article
from comments.forms import AddCommentForArticleForm
from comments.models import CommentForArticle
from comments.tasks import send_telegram_message


@require_POST
def add_new_comment_for_article(request, article_pk):
    last_comment_time = request.session.get('last_comment_time')
    if last_comment_time:
        since_comment_time = timezone.now() - timezone.datetime.fromisoformat(last_comment_time)
        if since_comment_time.total_seconds() < 60:
            return JsonResponse({
                'status': 'error',
                'message': 'Вы не можете оставлять комментарий чаще, чем раз в минуту. Попробуйте позже.'
            })
    article = get_object_or_404(Article, pk=article_pk)
    form = AddCommentForArticleForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.article = article
        new_comment.save()
        send_telegram_message.delay(
            chat_id=settings.COMMENTS_FROM_VER_G_CHAT_ID,
            comment_id=new_comment.id,
            message=f'На сайте ver-g.ru оставлен комментарий под статьей: *{article}*;\n----------\n'
                    f'Номер комментария: *{new_comment.id}*;\n----------\n'
                    f'Имя отправителя: *{new_comment.author}*;\n----------\n'
                    f'Текст комментария:\n'
                    f'"_{new_comment.text}_"\n\n----------\n'
                    f'ссылка на статью: (https://ver-g.ru{article.get_absolute_url()})')
        request.session['last_comment_time'] = timezone.now().isoformat()
        return JsonResponse({
            'status': 'success',
            'message': 'Сообщение отправлено. Оно будет опубликовано с минуты на минуту.'
        })
    return JsonResponse({
        'status': 'error',
        'message': 'Форма не валидна.'
    })


@require_POST
def add_answer_for_comment(request, article_pk, parent_pk):
    last_comment_time = request.session.get('last_comment_time')
    if last_comment_time:
        since_comment_time = timezone.now() - timezone.datetime.fromisoformat(last_comment_time)
        if since_comment_time.total_seconds() < 60:
            return JsonResponse({
                'status': 'error',
                'message': 'Вы не можете оставлять комментарий чаще, чем раз в минуту. Попробуйте позже.'
            })
    article = get_object_or_404(Article, pk=article_pk)
    parent = get_object_or_404(CommentForArticle, pk=parent_pk)
    form = AddCommentForArticleForm(request.POST)
    if form.is_valid():
        it_first_answer = False if parent.answers.all().exists() else True
        new_answer = form.save(commit=False)
        new_answer.article = article
        new_answer.parent = parent
        new_answer.save()
        send_telegram_message.delay(
            chat_id=settings.COMMENTS_FROM_VER_G_CHAT_ID,
            comment_id=new_answer.id,
            message=f'На сайте ver-g.ru оставлен комментарий под статьей: *{article}*;\n----------\n'
                    f'Номер комментария: *{new_answer.id}*;\n----------\n'
                    f'Имя отправителя: *{new_answer.author}*;\n----------\n'
                    f'Текст комментария:\n'
                    f'"_{new_answer.text}_"\n\n----------\n'
                    f'ссылка на статью: (https://ver-g.ru{article.get_absolute_url()})')
        request.session['last_comment_time'] = timezone.now().isoformat()
        return JsonResponse({
            'status': 'success',
            'message': 'ответ на комментарий успешно добавлен',
            'parent': parent.pk,
            'it_first_answer': it_first_answer
        })


@csrf_exempt
def api_comment_delete(request, comment_id, tele_id):
    if tele_id in settings.VER_G_ADMIN_TELEGRAM_CHAT_IDS:
        try:
            CommentForArticle.objects.get(pk=comment_id).delete()
        except CommentForArticle.DoesNotExist:
            return JsonResponse({"error": "такого комментария нет"})

        return JsonResponse({"success": "Комментарий успешно удален."})
    else:
        return JsonResponse({"error": "нет прав на удаление"})

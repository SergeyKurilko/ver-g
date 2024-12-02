import json

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from blog.models import Article, Category
from django.http import JsonResponse
from blog.forms import GetConsultationForm
from blog.tasks import get_consultation_bot_message
from comments.forms import AddCommentForArticleForm
from datetime import timedelta
from django.middleware.csrf import get_token

from vertograd.asgi import application



def index_page(request):
    articles = Article.objects.filter(published=True).prefetch_related(
        'category')[:3]

    return render(request, 'blog/index.html', {
        'articles': articles,
        'canonical_url': reverse('blog:home')
    })


class ArticleListView(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'blog/articles_list.html'
    paginate_by = 6

    def get_queryset(self):
        if self.kwargs.get('category_slug'):
            category = get_object_or_404(Category,
                                         slug=self.kwargs['category_slug'])
            return Article.is_published.filter(category=category)
        else:
            return Article.is_published.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['canonical_url'] = reverse('blog:articles_list')
        if self.kwargs.get('category_slug'):
            category = get_object_or_404(Category,
                                         slug=self.kwargs['category_slug'])
            context['category'] = category
            context['title'] = f"Статьи на тему: {category.name}"
        else:
            context['title'] = "Все статьи"
        return context


def article_detail(request, article_slug):
    article = get_object_or_404(Article.objects.prefetch_related("comments"), slug=article_slug)
    article.views_counter += 1
    article.save()
    category = article.category
    add_comment_form = AddCommentForArticleForm()
    similar_articles = \
        Article.objects.filter(category=category).exclude(pk=article.pk)[:3]

    first_three_comments = article.comments.filter(parent=None)[0:3]
    url_for_rate = json.dumps(request.build_absolute_uri(reverse('blog:article_rate', args=[article.pk])))
    token_for_rate = json.dumps(get_token(request))

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        offset = int(request.GET.get('offset', 0))
        limit = 3
        comments = article.comments.filter(parent=None)[offset:offset+limit]

        comments_data = [{
            'author': comment.author,
            'text': comment.text,
            'published': (comment.published + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M'),
            'csrf_token_for_answer_form': get_token(request),
            'id': comment.id,
            'article_id': article.id,
            'answers_count': comment.answers.all().count(),
            'answers': [{
                'answer_author': answer.author,
                'answer_text': answer.text,
                'answer_published': (answer.published + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M')
            } for answer in comment.answers.all()]
        } for comment in comments]

        return JsonResponse({
            'comments': comments_data
        })

    return render(request,
                  template_name='blog/article_detail.html',
                  context={
                      'article': article,
                      'add_comment_form': add_comment_form,
                      'similar_articles': similar_articles,
                      'first_three_comments': first_three_comments,
                      'url_for_rate': url_for_rate,
                      'token_for_rate': token_for_rate,
                      'canonical_url': request.build_absolute_uri(article.get_absolute_url())
                  })


def article_rate(request, article_pk):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        rate = request.POST.get("rate", 0)
        article = get_object_or_404(Article, pk=article_pk)
        article.rate += int(rate)
        article.save()
        return JsonResponse({
            "status": "success"
        })


@require_POST
def get_consultation_view(request):
    form = GetConsultationForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        get_consultation_bot_message.delay(application=cd)
        return JsonResponse(
            data=
            {'success': 'Спасибо! Мы свяжемся с Вами в ближайшее время.'},
            status=200)
    else:
        errors = form.errors.as_json()
        return JsonResponse(data={'error': errors}, status=400)


def about_us_page(request):
    context = {
        'canonical_url': reverse('blog:about_us')
    }
    return render(request, 'blog/about_us.html', context)


def contacts_page_view(request):
    context = {
        'canonical_url': reverse('blog:contacts')
    }
    return render(request, 'blog/contacts.html', context)


def policy_page_view(request):
    context = {
        'canonical_url': reverse('blog:policy')
    }
    return render(request, 'blog/politica.html', context)


def oferta_page_view(request):
    context = {
        'canonical_url': reverse('blog:oferta')
    }
    return render(request, 'blog/oferta.html', context)


def terms_page_view(request):
    context = {
        'canonical_url': reverse('blog:terms')
    }
    return render(request, 'blog/terms.html', context)


def privacy_page_view(request):
    context = {
        'canonical_url': reverse('blog:privacy')
    }
    return render(request, 'blog/privacy.html', context)






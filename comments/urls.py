from django.urls import path
from comments.views import add_new_comment_for_article, add_answer_for_comment

app_name = 'comments'

urlpatterns = [
    path('add_new_comment_for_article/<int:article_pk>/',
         add_new_comment_for_article,
         name='add_new_comment_for_article'),
    path('add_answer_for_comment/<int:article_pk>/<int:parent_pk>/',
         add_answer_for_comment,
         name='add_answer_for_comment'),
]
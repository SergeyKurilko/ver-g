from django import forms
from comments.models import CommentForArticle


class AddCommentForArticleForm(forms.ModelForm):
    class Meta:
        model = CommentForArticle
        fields = ['author', 'text']

        widgets = {
            'author': forms.TextInput(attrs={
                'class': 'form-control w-50',
                'placeholder': 'Имя'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст сообщения'
            })
        }
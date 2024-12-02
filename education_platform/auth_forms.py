from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.template import loader

UserModel = get_user_model()


class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, min_length=2, required=False, widget=forms.TextInput(attrs={
        "name": "name",
        "autocomplete": "name",
        "class": "form-control",
        "placeholder": "Имя",
        "title": "Ваше имя"
    }))

    last_name = forms.CharField(max_length=100, min_length=2, required=False, widget=forms.TextInput(attrs={
        "name": "last_name",
        "autocomplete": "last_name",
        "class": "form-control mt-3",
        "placeholder": "Фамилия",
        "title": "Ваша фамилия"
    }))

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        "name": "email",
        "autocomplete": "email",
        "class": "form-control mt-3",
        "placeholder": "e-mail",
        "title": "Ваш email"
    }))

    agreement = forms.BooleanField(required=True, widget=forms.CheckboxInput)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2", "agreement"]

    def save(self, commit=True):
        user = super(StudentRegistrationForm, self).save(commit=False)
        user.email = (self.cleaned_data["email"]).lower()
        user.first_name = (self.cleaned_data["first_name"]).capitalize()
        user.last_name = (self.cleaned_data["last_name"]).capitalize()
        user.username = f"student_{self.cleaned_data['email']}"
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(StudentRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            "class": "form-control mt-3",
            "placeholder": "пароль"
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            "class": "form-control mt-3",
            "placeholder": "пароль еще раз"
        })

    def clean_email(self):
        email = (self.cleaned_data['email']).lower()

        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже зарегистрирован. \n'
                                        '<a href="" id="passwordResetEducationPlatform" '
                                        'data-bs-toggle="modal" data-bs-target="'
                                        '#passwordResetModal">Сбросить пароль.</a></div>')

        return email


class StudentLoginForm(AuthenticationForm):
    # Заменим поле username на emailfield, т.к. Student будет регистрироваться и входить через email
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        "class": "form-control",
        "autocomplete": "email",
        "placeholder": "e-mail"
    }))

    class Meta:
        model = User
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super(StudentLoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput(attrs={
            "class": "form-control mt-3",
            "autocomplete": "password",
            "placeholder": "пароль"
        })

    def clean_username(self):
        username = (self.cleaned_data['username']).lower()

        if not UserModel.objects.filter(email=username):
            raise forms.ValidationError(f'Пользователь с email: {username} не зарегистрирован.\n'
                                        f'<a class="ms-1" style="cursor: pointer;"'
                                        f'id="registerButtonEducationPlatform" '
                                        f'data-bs-toggle="modal" '
                                        f'data-bs-target="#registerFormModal">'
                                        f'Зарегистрироваться.'
                                        f'</a>')

        return username

    def clean_password(self):
        password = self.cleaned_data['password']

        if self.cleaned_data.get('username', False) is not False:
            username = self.cleaned_data['username']
            user = UserModel.objects.get(email=username)
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль.')

        return password


class StudentPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = (self.cleaned_data['email']).lower()

        if email:
            try:
                user = UserModel.objects.get(email=email)
            except UserModel.DoesNotExist:
                raise forms.ValidationError("Пользователь с таким email не найден.")

        return email

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        subject = loader.render_to_string(template_name=subject_template_name, context=context)
        body = loader.render_to_string(template_name=email_template_name, context=context)
        context['user'] = context['user'].pk
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.NO_REPLY_DEFAULT_FROM_EMAIL,
            recipient_list=[to_email,],
            fail_silently=False,
            html_message=html_email_template_name,
        )


class StudentSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(StudentSetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={
            "class": "form-control mb-2 mt-4",
            "autocomplete": "new-password",
            "placeholder": "Новый пароль"
        })
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={
            "class": "form-control mb-2 mt-4",
            "autocomplete": "new-password",
            "placeholder": "Новый пароль (еще раз)",
        })
from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordResetConfirmView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy

from education_platform.models import Student
from education_platform.auth_forms import StudentLoginForm, StudentRegistrationForm, StudentPasswordResetForm, \
    StudentSetPasswordForm
from education_platform.tasks import send_telegram_register_new_user


def student_register(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = StudentRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if not user.first_name:
                user.first_name = f'User{user.pk}'
                user.save()
            student = Student.objects.create(user=user)

            send_telegram_register_new_user.delay(new_user = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email
            })

            login(request, user, backend='education_platform.backends.EmailBackend')
            return JsonResponse({
                'status': 'success',
            })
        else:
            return JsonResponse({
                "status": "error",
                "form_errors": form.errors
            })
    else:
        return redirect("education_platform:home")


def student_login(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = StudentLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return JsonResponse({
                'status': 'success',
            })
        return JsonResponse({
            'status': 'error',
            'login_form_errors': form.errors
        })
    return redirect("education_platform:home")


def student_logout(request):
    logout(request)
    return redirect("education_platform:home")


def password_reset_ajax(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = StudentPasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                email_template_name='education_platform/password_reset_email/password_reset_email.html',
                subject_template_name='education_platform/password_reset_email/password_reset_subject.txt'
            )
            return JsonResponse({
                'status': 'success'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'password_reset_form_errors': form.errors
            })
    else:
        return redirect("education_platform:home")


class StudentPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'education_platform/password_reset_email/student_password_reset_confirm.html'
    form_class = StudentSetPasswordForm
    success_url = reverse_lazy('education_platform:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['register_form'] = StudentRegistrationForm()
        context['login_form'] = StudentLoginForm()
        context['uidb64'] = self.kwargs['uidb64']  # Добавляем uidb64 в контекст
        context['token'] = self.kwargs['token']
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if form.is_valid():
                self.form_valid(form)
                return JsonResponse({
                    'status': 'success',
                    'success_url': reverse_lazy("education_platform:home")
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'reset_password_form_errors': form.errors
                })

        return redirect("education_platform:home")
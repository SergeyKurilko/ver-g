from io import BytesIO
import fitz

from django.http import HttpResponse, FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from weasyprint import HTML

from education_platform.auth_forms import StudentLoginForm, StudentRegistrationForm
from education_platform.models import CourseProgress


def get_certificate_detail(request, progress_pk):
    progress = get_object_or_404(CourseProgress, pk=progress_pk)

    # Если запрошено получение сертификата на незавершенный курс, то редирект на домашнюю
    if not progress.is_completed:
        return redirect('education_platform:home')

    context = {
        "progress": progress,
        'student_name': f"{progress.student.user.first_name} {progress.student.user.last_name}",
        'course_name': progress.training_course.title,
        'certificate_link': request.build_absolute_uri(),
    }

    # Если зашедший пользователь не залогинен, то передаем формы для регистрации / авторизации
    if not request.user.is_authenticated:
        context['login_form'] = StudentLoginForm
        context['register_form'] = StudentRegistrationForm

    return render(request,
                  'education_platform/get_certificate_page.html',
                  context)


def generate_certificate_pdf(request, progress):
    """
    Генерирует PDF сертификата с использованием WeasyPrint.
    """
    context = {
        'cert_num': progress.pk,
        'student_name': f"{progress.student.user.first_name} {progress.student.user.last_name}",
        'course_name': progress.training_course.title,
        'course_author': progress.training_course.author,
        'completed_date': progress.completed_date,
        'author_title': progress.training_course.author_title,
        'author_signature': progress.training_course.signature.url,
    }

    # Генерация HTML из шаблона
    html_string = render_to_string(
        'education_platform/certificate_templates/certificate_template.html',
        context=context,
        request=request
    )

    # Генерация PDF с использованием WeasyPrint
    pdf_file = BytesIO()
    HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf(pdf_file)

    return pdf_file.getvalue()


def download_certificate(request, progress_pk):
    # Объект CourseProgress для заполнения сертификата
    progress = CourseProgress.objects.get(pk=progress_pk)

    certificate_pdf = generate_certificate_pdf(request, progress)

    # Формируем имя файла с использованием progress_pk
    filename = f"VER-G_ACADEMY_Cert_{progress_pk}.pdf"

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.write(certificate_pdf)
    return response


def serve_certificate_image(request, progress_pk):
    """
    Создает временный url для изображения сертификата
    """
    progress = get_object_or_404(CourseProgress, pk=progress_pk)

    certificate_pdf = generate_certificate_pdf(request, progress)

    # Преобразование PDF в изображение с использованием PyMuPDF
    pdf_document = fitz.open(stream=certificate_pdf, filetype="pdf")
    page = pdf_document.load_page(0)  # Загрузка первой страницы

    # Увеличение разрешения изображения
    zoom_x = 1.2  # Коэффициент масштабирования по оси X
    zoom_y = 1.2 # Коэффициент масштабирования по оси Y
    mat = fitz.Matrix(zoom_x, zoom_y)
    pix = page.get_pixmap(matrix=mat)

    # Получаем изображение в виде байтовой строки
    image_bytes = pix.tobytes(output="png")

    # Возвращаем изображение в ответе
    return FileResponse(BytesIO(image_bytes), content_type='image/png')






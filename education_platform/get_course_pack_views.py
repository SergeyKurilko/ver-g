from django.http import JsonResponse
from django.template.loader import render_to_string

from education_platform.models import CoursePack


def get_paid_course_pack_ajax_view(request, course_pack_pk):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':

        # Если не авторизован
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': f'not_authenticated'
            })

        course_pack = CoursePack.objects.get(pk=course_pack_pk)
        courses = [course for course in course_pack.courses.all()]

        context = {
            "product_type": "course_pack",
            "product_id": course_pack.pk,
            "amount": course_pack.price,
            "course_pack_title": course_pack.title,
            "user_email": request.user.email,
            "courses": courses
        }
        modal_content = render_to_string(
            template_name='education_platform/incl/modal_for_get_course_pack.html',
            context=context,
            request=request)

        return JsonResponse({
            "success": "payment_course_pack_form",
            "payment_course_pack_form_modal": modal_content
        })

from django.urls import path
from django.contrib.auth import views as auth_views

from education_platform.comments_views import add_answer_for_comment_for_step_view, add_new_comment_for_step_ajax_view, \
    get_answers_for_comment
from education_platform.course_process_views import next_step_ajax_view, \
    get_step_detail_view, ajax_make_step_is_completed, \
    ajax_check_answer_for_question
from education_platform.get_certificate_views import get_certificate_detail, generate_certificate_pdf, \
    download_certificate, serve_certificate_image
from education_platform.get_course_pack_views import get_paid_course_pack_ajax_view
from education_platform.payments import create_transaction_view, transaction_callback, check_payment_status
from education_platform.views import EducationPlatformHomeView, \
    TrainingCourseDetailView, CoursePackDetailView, course_pack_list, course_list_view, get_cert_test_page
from education_platform.auth_views import student_login, student_logout, student_register, password_reset_ajax, \
    StudentPasswordResetConfirmView
from education_platform.get_course_views import get_course_ajax_view, get_paid_course_ajax_view, \
    payment_successful_view, use_promo_code_view, ajax_get_course_free_with_promo
from education_platform.personal_account_views import get_my_personal_account, avatar_upload_ajax, \
    update_personal_data_ajax, my_courses_view, my_certificates

app_name = 'education_platform'

urlpatterns = [
    path('', EducationPlatformHomeView.as_view(), name='home'),
    path('courses/all/', course_list_view, name='get_all_courses'),
    path('courses/<slug:course_slug>/',
         TrainingCourseDetailView.as_view(), name='course_detail'),
    path('course_packs/all/',
         course_pack_list, name='course_pack_list'),
    path('course_packs/<slug:course_pack_slug>/',
         CoursePackDetailView.as_view(), name='course_pack_detail'),
    path('login/', student_login, name="login"),
    path('logout/', student_logout, name="logout"),
    path('register/', student_register, name="register"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/',
         StudentPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_reset_ajax/', password_reset_ajax, name='password_reset_ajax'),
    path('course/progress/<int:course_pk>/<int:step_pk>/', get_step_detail_view, name='get_step_detail_view'),
    path('personal_account/', get_my_personal_account, name='get_my_personal_account'),
    path('personal_account/my_courses/', my_courses_view, name='my_courses'),
    path('personal_account/my_certificates/', my_certificates, name='my_certificates'),
    path('cert/<int:progress_pk>/', get_certificate_detail, name="get_certificate"),
    path('download-certificate/<int:progress_pk>/', download_certificate, name='download_certificate'),
    path('certificate/<int:progress_pk>/image', serve_certificate_image, name='serve_certificate_image'),
    path('get_cert_test_page/<int:progress_pk>', get_cert_test_page)
]

ajax_urlpatterns = [
    path('courses/lesson/next_step/',
         next_step_ajax_view, name='next_step_ajax'),
    path('payment/create_transaction/',
         create_transaction_view,
         name='create_transaction'),
    path('payment/transaction_callback/',
         transaction_callback,
         name='transaction_callback'),
    path('payment/successful/<slug:product_type>/<int:product_id>/',
         payment_successful_view,
         name='course_payment_successful'),
    path('payment/check_payment_status/<slug:payment_id>',
         check_payment_status,
         name='check_payment_status'),
    path('courses/get_course/<int:course_pk>/',
         get_course_ajax_view,
         name='get_course'),
    path('courses/get_paid_course/<int:course_pk>/',
         get_paid_course_ajax_view,
         name='get_paid_course'),
    path('ajax_make_step_is_completed/',
         ajax_make_step_is_completed,
         name='ajax_make_step_is_completed'),
    path('ajax_check_answer_for_question/',
         ajax_check_answer_for_question,
         name='ajax_check_answer_for_question'),
    path('personal_account/avatar_upload/',
         avatar_upload_ajax,
         name='avatar_upload'),
    path('personal_account/update_personal_data_ajax/',
         update_personal_data_ajax,
         name='update_personal_data'),
    path('course/progress/<int:step_pk>/ajax_add_comment',
         add_new_comment_for_step_ajax_view,
         name='ajax_add_new_comment_for_step'),
    path('course/progress/ajax_add_answer_for_comment/<int:comment_pk>/',
         add_answer_for_comment_for_step_view,
         name='ajax_add_answer_for_comment'),
    path('course/progress/ajax_get_answers_for_comment/<int:comment_pk>/',
         get_answers_for_comment,
         name='get_answers_for_comment'
         ),
    path('course_pack/get_paid_course_pack/<int:course_pack_pk>/',
         get_paid_course_pack_ajax_view,
         name="get_paid_course_pack"),
    path('ajax/use_promo_code_view',
         use_promo_code_view,
         name='use_promo_code'),
    path('ajax/ajax_get_course_free_with_promo',
         ajax_get_course_free_with_promo,
         name='ajax_get_course_free_with_promo')
]

urlpatterns += ajax_urlpatterns

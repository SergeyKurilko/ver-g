from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import TrainingCourseViewSet, CreatePromoFromTelegramBot, CheckPromoCodeApiView, EducationPlatformReport, \
    CommentForArticleDelete

app_name = "api"

router = DefaultRouter()
router.register(r'training_courses_query', TrainingCourseViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('create_promo_from_bot/', CreatePromoFromTelegramBot.as_view()),
    path('check_promo_from_bot/', CheckPromoCodeApiView.as_view()),
    path('education_platform_get_report/', EducationPlatformReport.as_view()),
    path('delete_comment_for_article/', CommentForArticleDelete.as_view())
]
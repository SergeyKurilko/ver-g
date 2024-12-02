from django.urls import path
from reviews.views import ReviewsListView, review_detail_view

app_name = "reviews"


urlpatterns = [
    path("all/", ReviewsListView.as_view(), name="reviews_list"),
    path("<slug:review_slug>", review_detail_view, name="review_detail"),
]
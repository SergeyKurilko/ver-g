from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from reviews.models import Review


class ReviewsListView(ListView):
    template_name = "reviews/reviews_list.html"
    model = Review
    queryset = Review.objects.all()
    context_object_name = "reviews"
    paginate_by = 6


def review_detail_view(request, review_slug):
    review = get_object_or_404(Review, slug=review_slug)
    return render(request, 'reviews/review_detail.html',
                  {'review': review})

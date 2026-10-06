from django.urls import resolve, reverse
from core_apps.ratings.views import RatingCreateAPIView


def test_create_rating_url():
    url = reverse("rating-create")
    assert url == "/api/v1/ratings/create/"
    assert resolve(url).func.view_class == RatingCreateAPIView
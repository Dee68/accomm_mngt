import pytest
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from core_apps.posts.models import Post
from core_apps.common.models import ContentView

User = get_user_model()


@pytest.mark.django_db
def test_top_posts_returns_zero_view_count_for_post_without_views():
    user = User.objects.create_user(
        username="top_post_user",
        email="top_post_user@example.com",
        password="TestPassword123!",
    )

    post = Post.objects.create(
        title="Post Without Views",
        body="Testing top posts.",
        author=user,
    )

    client = APIClient()
    response = client.get("/api/v1/posts/top-posts/")

    assert response.status_code == 200

    post_data = next(
        item for item in response.data["results"]
        if item["id"] == str(post.id)
    )

    assert post_data["view_count"] == 0

@pytest.mark.django_db
def test_top_posts_returns_correct_view_count():
    user = User.objects.create_user(
        username="view_count_user",
        email="view_count_user@example.com",
        password="TestPassword123!",
    )

    post = Post.objects.create(
        title="Post With Views",
        body="Testing view count.",
        author=user,
    )

    ContentView.record_view(
        content_object=post,
        user=user,
        viewer_ip="192.168.1.10",
    )

    client = APIClient()
    response = client.get("/api/v1/posts/top-posts/")

    assert response.status_code == 200

    post_data = next(
        item for item in response.data["results"]
        if item["id"] == str(post.id)
    )

    assert post_data["view_count"] == 1

@pytest.mark.django_db
def test_post_detail_records_content_view():
    user = User.objects.create_user(
        username="detail_view_user",
        email="detail_view_user@example.com",
        password="TestPassword123!",
    )

    post = Post.objects.create(
        title="Detail View Test",
        body="Testing post detail views.",
        author=user,
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get(
        f"/api/v1/posts/{post.slug}/",
        REMOTE_ADDR="192.168.1.20",
    )

    assert response.status_code == 200

    content_type = ContentType.objects.get_for_model(post)

    content_view = ContentView.objects.get(
        content_type=content_type,
        object_id=post.id,
        user=user,
        viewer_ip="192.168.1.20",
    )

    assert content_view.object_id == post.id
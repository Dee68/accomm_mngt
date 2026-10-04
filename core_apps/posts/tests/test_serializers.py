import pytest
from django.db.models import Count
from core_apps.posts.models import Post
from core_apps.posts.serializers import PopularTagSerializer, TopPostSerializer
from core_apps.users.models import User


@pytest.mark.django_db
def test_top_post_serializer():
    user = User.objects.create_user(
        username="postauthor",
        email="postauthor@example.com",
        password="TestPassword123!",
    )

    post = Post.objects.create(
        title="Top Post",
        body="Top post body.",
        author=user,
    )

    post = (
        Post.objects.annotate(
            replies_count=Count("replies"),
        )
        .get(pk=post.pk)
    )

    post.view_count = 0

    serializer = TopPostSerializer(instance=post)

    data = serializer.data

    assert data["id"] == str(post.id)
    assert data["title"] == "Top Post"
    assert data["slug"] == "top-post"
    assert data["author_username"] == "postauthor"
    assert data["upvotes"] == 0
    assert data["replies_count"] == 0
    assert data["view_count"] == 0
    assert data["avatar"] is None
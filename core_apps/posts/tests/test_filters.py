import pytest

from django.db.models import Count
from core_apps.posts.filters import PostFilter
from core_apps.posts.models import Post, Reply
from core_apps.users.models import User


@pytest.mark.django_db
def test_filter_posts_by_author_username():
    user1 = User.objects.create_user(
        username="johnsmith",
        email="john@example.com",
        password="TestPassword123!",
    )
    user2 = User.objects.create_user(
        username="janedoe",
        email="jane@example.com",
        password="TestPassword123!",
    )

    post1 = Post.objects.create(
        title="John's Post",
        body="Post written by John.",
        author=user1,
    )
    Post.objects.create(
        title="Jane's Post",
        body="Post written by Jane.",
        author=user2,
    )

    queryset = Post.objects.all()

    post_filter = PostFilter(
        data={"author_username": "JOHN"},
        queryset=queryset,
    )

    assert post_filter.is_valid()
    assert list(post_filter.qs) == [post1]

@pytest.mark.django_db
def test_filter_posts_by_tag():
    user = User.objects.create_user(
        username="taguser",
        email="taguser@example.com",
        password="TestPassword123!",
    )

    post1 = Post.objects.create(
        title="Python Post",
        body="A post about Python.",
        author=user,
    )
    post1.tags.add("python", "django")

    post2 = Post.objects.create(
        title="JavaScript Post",
        body="A post about JavaScript.",
        author=user,
    )
    post2.tags.add("javascript")

    post_filter = PostFilter(
        data={"tags": ["python"]},
        queryset=Post.objects.all(),
    )

    assert post_filter.is_valid()
    assert list(post_filter.qs) == [post1]

@pytest.mark.django_db
def test_filter_posts_most_replied_to():
    user = User.objects.create_user(
        username="replyuser",
        email="replyuser@example.com",
        password="TestPassword123!",
    )

    post_with_replies = Post.objects.create(
        title="Post With Replies",
        body="This post has replies.",
        author=user,
    )

    post_without_replies = Post.objects.create(
        title="Post Without Replies",
        body="This post has no replies.",
        author=user,
    )

    Reply.objects.create(
        post=post_with_replies,
        author=user,
        body="First reply",
    )

    post_filter = PostFilter(
        data={"most_replied_to": "true"},
        queryset=Post.objects.all(),
    )

    assert post_filter.is_valid()
    assert list(post_filter.qs) == [post_with_replies]

@pytest.mark.django_db
def test_filter_most_replied_to_false_returns_all_posts():
    user = User.objects.create_user(
        username="replyfalseuser",
        email="replyfalseuser@example.com",
        password="TestPassword123!",
    )

    post_with_replies = Post.objects.create(
        title="Post With Replies",
        body="This post has replies.",
        author=user,
    )

    post_without_replies = Post.objects.create(
        title="Post Without Replies",
        body="This post has no replies.",
        author=user,
    )

    Reply.objects.create(
        post=post_with_replies,
        author=user,
        body="A reply",
    )

    post_filter = PostFilter(
        data={"most_replied_to": "false"},
        queryset=Post.objects.all(),
    )

    assert post_filter.is_valid()
    assert set(post_filter.qs) == {
        post_with_replies,
        post_without_replies,
    }

@pytest.mark.django_db
def test_filter_ordering_oldest():
    user = User.objects.create_user(
        username="oldestuser",
        email="oldest@example.com",
        password="TestPassword123!",
    )

    oldest = Post.objects.create(
        title="Oldest Post",
        body="Oldest post.",
        author=user,
    )

    middle = Post.objects.create(
        title="Middle Post",
        body="Middle post.",
        author=user,
    )

    newest = Post.objects.create(
        title="Newest Post",
        body="Newest post.",
        author=user,
    )

    post_filter = PostFilter(
        data={"ordering": "oldest"},
        queryset=Post.objects.all(),
    )

    assert post_filter.is_valid()
    assert list(post_filter.qs) == [oldest, middle, newest]


@pytest.mark.django_db
def test_filter_ordering_most_recent():
    user = User.objects.create_user(
        username="recentuser",
        email="recent@example.com",
        password="TestPassword123!",
    )

    oldest = Post.objects.create(
        title="Oldest Post",
        body="Oldest post.",
        author=user,
    )

    middle = Post.objects.create(
        title="Middle Post",
        body="Middle post.",
        author=user,
    )

    newest = Post.objects.create(
        title="Newest Post",
        body="Newest post.",
        author=user,
    )

    post_filter = PostFilter(
        data={"ordering": "most_recent"},
        queryset=Post.objects.all(),
    )

    assert post_filter.is_valid()
    assert list(post_filter.qs) == [newest, middle, oldest]

@pytest.mark.django_db
def test_filter_ordering_most_replied_to():
    user = User.objects.create_user(
        username="orderinguser",
        email="ordering@example.com",
        password="TestPassword123!",
    )

    post_one_reply = Post.objects.create(
        title="One Reply",
        body="One reply post.",
        author=user,
    )

    post_three_replies = Post.objects.create(
        title="Three Replies",
        body="Three replies post.",
        author=user,
    )

    post_no_replies = Post.objects.create(
        title="No Replies",
        body="No replies post.",
        author=user,
    )

    Reply.objects.create(
        post=post_one_reply,
        author=user,
        body="Reply 1",
    )

    for number in range(3):
        Reply.objects.create(
            post=post_three_replies,
            author=user,
            body=f"Reply {number + 1}",
        )

    queryset = Post.objects.annotate(
        replies_count=Count("replies")
    )

    post_filter = PostFilter(
        data={"ordering": "most_replied_to"},
        queryset=queryset,
    )

    assert post_filter.is_valid()
    assert list(post_filter.qs) == [
        post_three_replies,
        post_one_reply,
        post_no_replies,
    ]
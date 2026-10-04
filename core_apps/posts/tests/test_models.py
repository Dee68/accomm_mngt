import pytest

from core_apps.posts.models import Post, Reply
from core_apps.users.models import User
from core_apps.profiles.models import Profile
from core_apps.common.models import ContentView


@pytest.mark.django_db
def test_post_can_be_created():
    user = User.objects.create_user(
        username="postauthor",
        email="postauthor@example.com",
        password="TestPassword123!",
    )

    post = Post.objects.create(
        title="Test Post",
        body="This is a test post.",
        author=user,
    )

    assert post.title == "Test Post"
    assert post.body == "This is a test post."
    assert post.author == user


@pytest.mark.django_db
def test_post_string_representation():
    user = User.objects.create_user(
        username="postauthor",
        email="postauthor@example.com",
        password="TestPassword123!",
    )

    post = Post.objects.create(
        title="My Test Post",
        body="Test body",
        author=user,
    )

    assert str(post) == "My Test Post"


@pytest.mark.django_db
def test_post_generates_slug_from_title():
    user = User.objects.create_user(
        username="postauthor",
        email="postauthor@example.com",
        password="TestPassword123!",
    )

    post = Post.objects.create(
        title="My Test Post",
        body="Test body",
        author=user,
    )

    assert post.slug == "my-test-post"


@pytest.mark.django_db
def test_post_default_vote_counts():
    user = User.objects.create_user(
        username="postauthor",
        email="postauthor@example.com",
        password="TestPassword123!",
    )

    post = Post.objects.create(
        title="Test Post",
        body="Test body",
        author=user,
    )

    assert post.upvotes == 0
    assert post.downvotes == 0


@pytest.mark.django_db
def test_post_bookmarks_relationship():
    author = User.objects.create_user(
        username="postauthor",
        email="postauthor@example.com",
        password="TestPassword123!",
    )

    bookmark_user = User.objects.create_user(
        username="bookmarkuser",
        email="bookmark@example.com",
        password="TestPassword123!",
    )

    post = Post.objects.create(
        title="Bookmarked Post",
        body="Test body",
        author=author,
    )

    post.bookmarked_by.add(bookmark_user)

    assert bookmark_user in post.bookmarked_by.all()
    assert post in bookmark_user.bookmarked_posts.all()


@pytest.mark.django_db
def test_post_upvotes_relationship():
    author = User.objects.create_user(
        username="postauthor",
        email="postauthor@example.com",
        password="TestPassword123!",
    )

    voting_user = User.objects.create_user(
        username="votinguser",
        email="voting@example.com",
        password="TestPassword123!",
    )

    post = Post.objects.create(
        title="Upvoted Post",
        body="Test body",
        author=author,
    )

    post.upvoted_by.add(voting_user)

    assert voting_user in post.upvoted_by.all()
    assert post in voting_user.upvoted_posts.all()


@pytest.mark.django_db
def test_post_downvotes_relationship():
    author = User.objects.create_user(
        username="postauthor",
        email="postauthor@example.com",
        password="TestPassword123!",
    )

    voting_user = User.objects.create_user(
        username="votinguser",
        email="voting@example.com",
        password="TestPassword123!",
    )

    post = Post.objects.create(
        title="Downvoted Post",
        body="Test body",
        author=author,
    )

    post.downvoted_by.add(voting_user)

    assert voting_user in post.downvoted_by.all()
    assert post in voting_user.downvoted_posts.all()


@pytest.mark.django_db
def test_reply_can_be_created():
    user = User.objects.create_user(
        username="replyauthor",
        email="replyauthor@example.com",
        password="TestPassword123!",
    )

    post = Post.objects.create(
        title="Test Post",
        body="Test body",
        author=user,
    )

    reply = Reply.objects.create(
        post=post,
        author=user,
        body="This is a test reply.",
    )

    assert reply.post == post
    assert reply.author == user
    assert reply.body == "This is a test reply."


@pytest.mark.django_db
def test_reply_string_representation():
    user = User.objects.create_user(
        username="replyauthor",
        email="replyauthor@example.com",
        password="TestPassword123!",
    )

    post = Post.objects.create(
        title="Test Post",
        body="Test body",
        author=user,
    )

    reply = Reply.objects.create(
        post=post,
        author=user,
        body="This is a test reply.",
    )

    assert str(reply) == "Reply by replyauthor on Test Post"


@pytest.mark.django_db
def test_deleting_post_deletes_replies():
    user = User.objects.create_user(
        username="replyauthor",
        email="replyauthor@example.com",
        password="TestPassword123!",
    )

    post = Post.objects.create(
        title="Test Post",
        body="Test body",
        author=user,
    )

    reply = Reply.objects.create(
        post=post,
        author=user,
        body="This is a test reply.",
    )

    reply_pk = reply.pk

    post.delete()

    assert not Reply.objects.filter(pk=reply_pk).exists()


@pytest.mark.django_db
def test_tenant_can_create_post():
    user = User.objects.create_user(
        username="tenantuser",
        email="tenant@example.com",
        password="TestPassword123!",
    )

    user.profile.occupation = Profile.Occupation.TENANT
    user.profile.save()

    post = Post.objects.create(
        title="Tenant Post",
        body="Post created by a tenant.",
        author=user,
    )

    assert post.author == user


@pytest.mark.django_db
def test_staff_user_can_create_post():
    user = User.objects.create_user(
        username="staffuser",
        email="staff@example.com",
        password="TestPassword123!",
        is_staff=True,
    )

    post = Post.objects.create(
        title="Staff Post",
        body="Post created by staff.",
        author=user,
    )

    assert post.author == user


@pytest.mark.django_db
def test_superuser_can_create_post():
    user = User.objects.create_superuser(
        username="superuser",
        email="superuser@example.com",
        password="TestPassword123!",
    )

    post = Post.objects.create(
        title="Superuser Post",
        body="Post created by a superuser.",
        author=user,
    )

    assert post.author == user


@pytest.mark.django_db
def test_non_tenant_non_staff_non_superuser_cannot_create_post():
    user = User.objects.create_user(
        username="regularuser",
        email="regular@example.com",
        password="TestPassword123!",
    )

    user.profile.occupation = Profile.Occupation.PLUMBER
    user.profile.save()

    with pytest.raises(
        ValueError,
        match="Only tenants, superuser or staff members can create posts.",
    ):
        Post.objects.create(
            title="Unauthorized Post",
            body="This post should not be created.",
            author=user,
        )


@pytest.mark.django_db
def test_get_popular_tags_returns_tags_by_post_count():
    author = User.objects.create_user(
        username="tagauthor",
        email="tagauthor@example.com",
        password="TestPassword123!",
    )

    post1 = Post.objects.create(
        title="First Post",
        body="First post body.",
        author=author,
    )
    post1.tags.add("django", "python")

    post2 = Post.objects.create(
        title="Second Post",
        body="Second post body.",
        author=author,
    )
    post2.tags.add("django")

    popular_tags = list(Post.get_popular_tags(limit=5))

    assert popular_tags[0].name == "django"
    assert popular_tags[0].post_count == 2

@pytest.mark.django_db
def test_post_content_views_generic_relation():
    author = User.objects.create_user(
        username="viewauthor",
        email="viewauthor@example.com",
        password="TestPassword123!",
    )

    viewer = User.objects.create_user(
        username="viewer",
        email="viewer@example.com",
        password="TestPassword123!",
    )

    post = Post.objects.create(
        title="Viewed Post",
        body="Post body.",
        author=author,
    )

    ContentView.record_view(
        content_object=post,
        user=viewer,
        viewer_ip="192.168.1.10",
    )

    assert post.content_views.count() == 1
    assert post.content_views.first().user == viewer
    assert post.content_views.first().viewer_ip == "192.168.1.10"

@pytest.mark.django_db
def test_deleting_post_author_deletes_posts():
    user = User.objects.create_user(
        username="postauthor",
        email="postauthor@example.com",
        password="TestPassword123!",
    )

    post = Post.objects.create(
        title="Author's Post",
        body="Post body.",
        author=user,
    )

    post_pk = post.pk

    user.delete()

    assert not Post.objects.filter(pk=post_pk).exists()



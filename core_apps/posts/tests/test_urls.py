import pytest

from django.urls import resolve

from core_apps.posts.views import (
    PostListAPIView,
    PostCreateAPIView,
    PostDetailAPIView,
    PostsByTagListAPIView,
    PostUpdateAPIView,
    MyPostListAPIView,
    BookmarkedPostListAPIView,
    BookmarkPostAPIView,
    UnBookmarkPostAPIView,
    UpvotePostAPIView,
    ReplyListAPIView,
    ReplyCreateAPIView,
    DownvotePostAPIView,
    TopPostListAPIView,
    PopularTagsListAPIView,
)

@pytest.mark.parametrize(
    "url, expected_view",
    [
        ("", PostListAPIView),
        ("tags/test-tag/", PostsByTagListAPIView),
        ("top-posts/", TopPostListAPIView),
        ("popular-tags/", PopularTagsListAPIView),
        ("create/", PostCreateAPIView),
        ("my-posts/", MyPostListAPIView),
        ("test-post/", PostDetailAPIView),
        ("test-post/update/", PostUpdateAPIView),
        ("test-post/bookmark/", BookmarkPostAPIView),
        ("test-post/unbookmark/", UnBookmarkPostAPIView),
        ("bookmarked/posts/", BookmarkedPostListAPIView),
        ("550e8400-e29b-41d4-a716-446655440000/reply/", ReplyCreateAPIView),
        ("550e8400-e29b-41d4-a716-446655440000/replies/", ReplyListAPIView),
        ("550e8400-e29b-41d4-a716-446655440000/upvote/", UpvotePostAPIView),
        ("550e8400-e29b-41d4-a716-446655440000/downvote/", DownvotePostAPIView),
    ],
)

def test_posts_resolve_to_correct_views(url, expected_view):
    resolved = resolve(f"/api/v1/posts/{url}")

    assert resolved.func.view_class == expected_view
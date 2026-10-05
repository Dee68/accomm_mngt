import pytest

from django.urls import reverse


def test_issue_list_url():
    assert reverse("issue-list") == "/api/v1/issues/"


def test_my_issue_list_url():
    assert reverse("my-issue-list") == "/api/v1/issues/me/"


def test_assigned_issue_list_url():
    assert reverse("assigned-issues") == "/api/v1/issues/assigned/"


def test_create_issue_url():
    apartment_id = "12345678-1234-5678-1234-567812345678"

    assert reverse(
        "create-issue",
        kwargs={"apartment_id": apartment_id},
    ) == f"/api/v1/issues/create/{apartment_id}/"


def test_update_issue_url():
    issue_id = "12345678-1234-5678-1234-567812345678"

    assert reverse(
        "update-issue",
        kwargs={"id": issue_id},
    ) == f"/api/v1/issues/update/{issue_id}/"


def test_issue_detail_url():
    issue_id = "12345678-1234-5678-1234-567812345678"

    assert reverse(
        "issue-detail",
        kwargs={"id": issue_id},
    ) == f"/api/v1/issues/{issue_id}/"


def test_delete_issue_url():
    issue_id = "12345678-1234-5678-1234-567812345678"

    assert reverse(
        "delete-issue",
        kwargs={"id": issue_id},
    ) == f"/api/v1/issues/delete/{issue_id}/"

import json

import pytest
from rest_framework.response import Response

from core_apps.common.renderers import GenericJSONRenderer


@pytest.mark.django_db
def test_generic_json_renderer_wraps_response_data():
    renderer = GenericJSONRenderer()

    response = Response(
        {"message": "Hello world"},
        status=200,
    )

    renderer_context = {
        "response": response,
    }

    rendered = renderer.render(
        {"message": "Hello world"},
        renderer_context=renderer_context,
    )

    data = json.loads(rendered)

    assert data == {
        "status_code": 200,
        "object_label": "object",
        "data": {
            "message": "Hello world",
        },
    }

@pytest.mark.django_db
def test_generic_json_renderer_uses_view_object_label():
    renderer = GenericJSONRenderer()

    response = Response(
        {"name": "John"},
        status=200,
    )

    class TestView:
        object_label = "profile"

    renderer_context = {
        "view": TestView(),
        "response": response,
    }

    rendered = renderer.render(
        {"name": "John"},
        renderer_context=renderer_context,
    )

    data = json.loads(rendered)

    assert data["status_code"] == 200
    assert data["object_label"] == "profile"
    assert data["data"] == {"name": "John"}

def test_generic_json_renderer_returns_errors_unchanged():
    renderer = GenericJSONRenderer()

    error_data = {
        "errors": {
            "detail": "Invalid request"
        }
    }

    response = Response(error_data, status=400)
    renderer_context = {"response": response}

    rendered = renderer.render(
        error_data,
        renderer_context=renderer_context,
    )

    data = json.loads(rendered)

    assert data == error_data
    assert "status_code" not in data
    assert "object_label" not in data

def test_generic_json_renderer_requires_response_in_context():
    renderer = GenericJSONRenderer()

    with pytest.raises(
        ValueError,
        match="Response not found in renderer context",
    ):
        renderer.render(
            {"message": "Hello"},
            renderer_context={},
        )

def test_generic_json_renderer_requires_response_when_context_is_none():
    renderer = GenericJSONRenderer()

    with pytest.raises(
        ValueError,
        match="Response not found in renderer context",
    ):
        renderer.render(
            {"message": "Hello"},
            renderer_context=None,
        )

def test_generic_json_renderer_uses_response_status_code():
    renderer = GenericJSONRenderer()

    response = Response(
        {"message": "Created successfully"},
        status=201,
    )

    renderer_context = {"response": response}

    rendered = renderer.render(
        {"message": "Created successfully"},
        renderer_context=renderer_context,
    )

    data = json.loads(rendered)

    assert data["status_code"] == 201
    assert data["object_label"] == "object"
    assert data["data"] == {"message": "Created successfully"}

def test_generic_json_renderer_does_not_wrap_errors_with_custom_object_label():
    renderer = GenericJSONRenderer()

    class TestView:
        object_label = "profile"

    error_data = {
        "errors": {
            "detail": "Authentication credentials were not provided."
        }
    }

    response = Response(error_data, status=401)

    renderer_context = {
        "view": TestView(),
        "response": response,
    }

    rendered = renderer.render(
        error_data,
        renderer_context=renderer_context,
    )

    data = json.loads(rendered)

    assert data == error_data
    assert "status_code" not in data
    assert "object_label" not in data
    assert "data" not in data
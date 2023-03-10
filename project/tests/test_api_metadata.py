"""Tests for the /metadata endpoint."""
# project/tests/test_metadata.py

from app.box_metadata_template import get_metadata_template_by_name
from tests.conftest import get_settings_override

settings = get_settings_override()


def test_metadata(test_app, box_client):
    """Should return a 404 if it does not exist or the metadata template details"""
    response = test_app.get("/metadata")

    template = get_metadata_template_by_name(
        box_client, settings.MEDIA_METADATA_TEMPLATE_NAME
    )
    if template is None:
        assert response.status_code == 404
        assert response.json() == {"detail": "Service template not found."}
    else:
        assert response.status_code == 200


def test_metadata_create(test_app, box_client):
    """Should create a metadata template"""
    template = get_metadata_template_by_name(
        box_client, settings.MEDIA_METADATA_TEMPLATE_NAME
    )
    if template is not None:
        template.delete()

    response = test_app.post("/metadata")
    assert response.status_code == 201

    template = get_metadata_template_by_name(
        box_client, settings.MEDIA_METADATA_TEMPLATE_NAME
    )
    assert template is not None

    result = template.response_object
    assert response.json() == {"status": "success", "data": result}


def test_metadata_create_already_exists(test_app):
    """Should return a 400 if the metadata template already exists"""
    response = test_app.post("/metadata")
    assert response.status_code == 400
    assert response.json() == {"detail": "Service template already exists."}


def test_metadata_create_force(test_app, box_client):
    """Should create a metadata template"""
    response = test_app.post("/metadata?force=true")
    assert response.status_code == 201

    template = get_metadata_template_by_name(
        box_client, settings.MEDIA_METADATA_TEMPLATE_NAME
    )
    assert template is not None

    result = template.response_object
    assert response.json() == {"status": "success", "data": result}


def test_metadata_get(test_app, box_client):
    """Should return the metadata template details"""
    response = test_app.get("/metadata")
    assert response.status_code == 200

    template = get_metadata_template_by_name(
        box_client, settings.MEDIA_METADATA_TEMPLATE_NAME
    )
    assert template is not None

    result = template.response_object
    assert response.json() == {"status": "success", "data": result}


def test_metadata_delete(test_app, box_client):
    """Should delete the metadata template"""
    response = test_app.delete("/metadata")
    assert response.status_code == 200

    template = get_metadata_template_by_name(
        box_client, settings.MEDIA_METADATA_TEMPLATE_NAME
    )
    assert template is None
    assert response.json() == {"status": "success"}

    # and if we delete again then it should return a 404
    response = test_app.delete("/metadata")
    assert response.status_code == 404

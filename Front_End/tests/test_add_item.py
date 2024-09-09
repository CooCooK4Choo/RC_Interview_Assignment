import pytest
from unittest.mock import patch, MagicMock
from flask import url_for
from app import app


@pytest.fixture
def client():
    """Fixture to simulate client."""
    with app.test_client() as client:
        yield client


@patch("requests.post")
def test_add_item_post(mock_post, client):
    """Integration test for the /add_item POST route to ensure item is added and redirects correctly."""

    # Mock the POST request response
    mock_post.return_value.status_code = 200

    # Make a POST request
    response = client.post(
        url_for("add_item"),
        data={"title": "New Item", "description": "New Description"},
    )

    # Assertions
    assert response.status_code == 302  # Check if it redirects
    assert response.location == url_for(
        "index"
    )  # Check that it redirects to the /list page

    # Follow the redirect to check the content of the index page
    follow_response = client.get(response.location)
    assert follow_response.status_code == 200

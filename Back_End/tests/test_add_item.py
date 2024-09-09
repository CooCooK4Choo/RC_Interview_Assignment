import pytest
from unittest.mock import patch
from app import app


@pytest.fixture
def client():
    """Fixture to simulate client."""
    with app.test_client() as client:
        yield client


@patch("app.add_item")
def test_create_items_success(mock_add_item, client):
    """Test the create_items route when item is successfully created."""

    # Mock the add_item function to do nothing (simulate success)
    mock_add_item.return_value = None

    # Make a POST request to the /api/create/<title>/<description> route
    response = client.post("/api/create/TestTitle/TestDescription")

    # Assertions
    assert response.status_code == 200
    assert response.data == b"success"


@patch("app.add_item")
def test_create_items_error(mock_add_item, client):
    """Test the create_items route when an error occurs during creation."""

    # Mock the add_item function to raise an exception
    mock_add_item.side_effect = Exception("Database Error")

    # Make a POST request to the /api/create/<title>/<description> route
    response = client.post("/api/create/TestTitle/TestDescription")

    # Assertions
    assert response.status_code == 400
    assert response.data == b"Custom Error"

import pytest
from unittest.mock import patch
from app import app


@pytest.fixture
def client():
    """Fixture to simulate client."""
    with app.test_client() as client:
        yield client


@patch("app.get_all_items")
def test_get_items_success(mock_get_all_items, client):
    """Test the get_items route when data is successfully retrieved."""

    # Mock the get_all_items function to return test data
    mock_get_all_items.return_value = [
        ("Test Item 1", "Test Description 1"),
        ("Test Item 2", "Test Description 2"),
    ]

    # Make a GET request to the /api/items route
    response = client.get("/api/items")

    # Assertions
    assert response.status_code == 200
    assert response.json == [
        {"title": "Test Item 1", "description": "Test Description 1"},
        {"title": "Test Item 2", "description": "Test Description 2"},
    ]


@patch("app.get_all_items")
def test_get_items_no_data(mock_get_all_items, client):
    """Test the get_items route when no data is found."""

    # Mock the get_all_items function to return an empty list
    mock_get_all_items.return_value = []

    # Make a GET request to the /api/items route
    response = client.get("/api/items")

    # Assertions
    assert response.status_code == 404
    assert response.data == b"No data to retrieve, please create records"


@patch("app.get_all_items")
def test_get_items_error(mock_get_all_items, client):
    """Test the get_items route when an error occurs."""

    # Mock the get_all_items function to raise an exception
    mock_get_all_items.side_effect = Exception("Database Error")

    # Make a GET request to the /api/items route
    response = client.get("/api/items")

    # Assertions
    assert response.status_code == 200
    assert response.data == b"Custom Error"

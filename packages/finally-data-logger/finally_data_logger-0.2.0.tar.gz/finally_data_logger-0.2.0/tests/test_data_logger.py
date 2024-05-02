import pytest
from finally_data_logger import DataLogger
import numpy as np


@pytest.fixture
def client():
    """Fixture for initializing the client."""
    return DataLogger(port=5000)


def test_log_data(client):
    data = {
        "name": "test1",
        "duration": 0.3,
        "image": np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255]]),
    }
    response = client.log_data(data)
    assert "message" in response
    assert response["message"] == "Data logged successfully!"


def test_get_data(client):
    criteria = {"name": "test*"}
    results = client.get_data(criteria)
    assert isinstance(results, list)
    assert len(results) > 0


def test_reset_database(client):
    response = client.reset_database()
    assert "message" in response
    assert response["message"] == "Database and blobs reset successfully!"


def test_delete_data(client):
    criteria = {"name": "test1"}
    response = client.delete_data(criteria)
    assert "message" in response
    assert response["message"].startswith("Deleted")

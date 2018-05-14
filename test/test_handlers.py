from falcon import testing
from api.app import app
import pytest
from urllib.parse import urlencode


@pytest.fixture()
def client():
    return testing.TestClient(app)


def test_put_update(client):
    headers = {"Content-Type": "application/json"}
    todo = urlencode({"title": "Test PUT Update", "status": "In progress"})
    client.simulate_post('/todos', headers=headers, body=todo)

    update = urlencode({"title": "Test PUT Update...", "status": "Valid case done"})
    expected_resp = {"id": 1, "title": "Test PUT Update...", "status": "Valid case done"}
    result = client.simulate_put('/todos/1', headers=headers, body=update)
    assert result.json == expected_resp

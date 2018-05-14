import falcon
from api.app import app
import pytest


HEADERS = {"Content-Type": "application/json"}
todo_id = 0


@pytest.fixture()
def client():
    global todo_id
    client = falcon.testing.TestClient(app)

    todo = '{"title": "Test PUT Update", "status": "In progress"}'
    client.simulate_post('/todos', headers=HEADERS, body=todo)
    todo_id += 1

    return client


def test_put_update(client):
    global todo_id
    update = '{"title": "PUT Update Test", "status": "Valid case done"}'
    expected_resp = [{"id": todo_id, "title": "PUT Update Test", "status": "Valid case done"}]
    result = client.simulate_put('/todos/{}'.format(todo_id), headers=HEADERS, body=update)
    assert result.json == expected_resp


def test_update_title(client):
    global todo_id
    update = '{"title": "Test PUT Update title"}'
    expected_resp = [{"id": todo_id, "title": "Test PUT Update title", "status": "In progress"}]
    result = client.simulate_put('/todos/{}'.format(todo_id), headers=HEADERS, body=update)
    assert result.json == expected_resp


def test_update_status(client):
    global todo_id
    update = '{"status": "Valid case done"}'
    expected_resp = [{"id": todo_id, "title": "Test PUT Update", "status": "Valid case done"}]
    result = client.simulate_put('/todos/{}'.format(todo_id), headers=HEADERS, body=update)
    assert result.json == expected_resp


def test_update_empty_body(client):
    update = '{}'
    result = client.simulate_put('/todos/1', headers=HEADERS, body=update)
    assert result.status == falcon.HTTP_400


def test_update_invalid_id(client):
    update = '{"title": "PUT Update Test", "status": "Valid case done"}'
    result = client.simulate_put('/todos/999', headers=HEADERS, body=update)
    assert result.status == falcon.HTTP_400

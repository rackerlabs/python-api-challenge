from falcon import testing,falcon
import pytest
import json
from api.app import app

@pytest.fixture()
def client():
    # Assume the hypothetical `myapp` package has a function called
    # `create()` to initialize and return a `falcon.API` instance.
    return testing.TestClient(app)


def test_get_health(client):
    """
    this test the health of the app
    """
    result = client.simulate_get('/health')
    assert result.status == falcon.HTTP_OK

def test_put_todo_status(client):
    """
    this to test the update api
    """
    bod = {u"status":"active",u"title":"sample"}
    result = client.simulate_put('/todo/1',body=bod)
    status = {u"status":"active"}
    assert result.json == status
    assert result.status == falcon.HTTP_OK

def test_put_todo_message(client):
    """
    this to test the api message
    """
    bod = {u"stat":"active",u"title":"sample"}
    result = client.simulate_put('/todo/1',body=bod)
    message = {u'ERROR':'request doesnot have a title or status'}
    assert result.json == message
    assert result.status == falcon.HTTP_404

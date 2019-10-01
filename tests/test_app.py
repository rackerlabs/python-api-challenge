import sys
import falcon
from falcon import testing
import pytest

from api.app import app


@pytest.fixture
def client():
    return testing.TestClient(app)


# pytest will inject the object returned by the "client" function
# as an additional parameter.
def test_create(client):
    data = {'title': 'new todo', 'status': 'Uncompleted'}
    response = client.simulate_post('/todos/', json=data)
    assert response.status == falcon.HTTP_201
    result = response.json
    assert 'id' in result
    result.pop('id')
    assert result == data


def test_put(client):
    headers = {'content-type': 'application/json'}
    data = {'title': 'new todo', 'status': 'Uncompleted'}
    response = client.simulate_post('/todos/', json=data)
    assert response.status == falcon.HTTP_201
    todo = response.json
    # put an existing todo
    most_recent_id = todo['id']
    path = '/todos/{}/'.format(most_recent_id)
    data['status'] = 'Done'
    response = client.simulate_put(path, json=data, headers=headers)
    assert response.status == falcon.HTTP_OK

    # test put not found(int)
    most_recent_id = 9999999999999  # python 3 doesn't habe sys.maxint so let's use this big number for now
    path = '/todos/{}/'.format(most_recent_id)
    response = client.simulate_put(path, json=data, headers=headers)
    assert response.status == falcon.HTTP_404

    # test not found if we use an string instead of an integer in the route
    path = '/todos/{}/'.format('notint')
    response = client.simulate_put(path, json=data, headers=headers)
    assert response.status == falcon.HTTP_404

    # test malformed json: it should return 400
    most_recent_id = todo['id']
    path = '/todos/{}/'.format(most_recent_id)
    data['status'] = 'Done'
    response = client.simulate_put(path, body='bad json', headers=headers)
    assert response.status == falcon.HTTP_400
    assert response.content.startswith(b'Malformed JSON')

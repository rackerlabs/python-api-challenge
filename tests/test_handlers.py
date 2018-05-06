import falcon

def test_put(client):
    """
    Test For API update to database
    :param client:
    :return: status
    """
    data = {
        "status":"Online",
        "title":"TestA"
    }
    result = client.simulate_put('/todos/1', body=data)
    expected_data =  {
        "status": "Online",
    }
    assert result.json == expected_data
    assert result.status == falcon.HTTP_OK
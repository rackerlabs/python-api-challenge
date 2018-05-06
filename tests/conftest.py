import pytest
import falcon
from falcon import testing

from api.app import app

@pytest.fixture(scope="module")
def client():
    return testing.TestClient(app)
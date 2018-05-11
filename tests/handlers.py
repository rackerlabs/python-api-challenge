import falcon
from api.app import app
from falcon import testing


class BaseTestCase(testing.TestCase):
    """
    Loads the `falcon.API` instance.
    """

    def setUp(self):
        self.app = app


class TestTodoPut(BaseTestCase):
    """
    NOTE: Class depends on a record with id = 1. This class assumes no other
    records have been inserted.
    """

    original_record = {
        'title': 'Take out the trash.',
        'status': 'complete',
    }
    good_request = {
        'title': 'Pick up milk.',
        'status': 'incomplete',
    }

    @classmethod
    def setUpClass(cls):
        # Insert at least one record before starting
        cls.simulate_post('/todos/', body=cls.original_record)

    @classmethod
    def tearDownClass(self):
        # TODO: Should implement a way to refresh the database.
        pass

    def test_bad_request(self):
        """
        Route should handle malformed JSON bodies.
        """
        result = self.simulate_put('/todos/1/', body=':D')
        assert result.status == falcon.HTTP_400

    def test_good_request(self):
        """
        Route should return a body identical to the request.
        """
        result = self.simulate_put('/todos/1/', body=self.good_request)
        assert result.json == self.good_request

    def test_not_enough_keys(self):
        """
        Body must have both 'title' and 'status' keys in the body.
        """
        result = self.simulate_put('/todos/1/', body={
            'title': 'This only contains a title.',
        })
        assert result.status == falcon.HTTP_400

    def test_too_many_keys(self):
        """
        Route should only accept 'title' and 'status' keys in the body.
        """
        result = self.simulate_put('/todos/1/', body={
            'extra': 'read all about it',
            **self.good_request,
        })
        assert result.status == falcon.HTTP_400

    def test_bad_id(self):
        """
        Route id must be an integer.
        """
        result = self.simulate_put('/todos/a/', body=self.good_request)
        assert result.status == falcon.HTTP_400

    def test_id_not_found(self):
        """
        Route id must exist in the database.
        """
        result = self.simulate_put('/todos/-1/', body=self.good_request)
        assert result.status == falcon.HTTP_404

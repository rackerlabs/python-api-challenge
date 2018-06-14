import json
import falcon

from config.settings import API_DEFAULT_LIMIT


class HealthHandler(object):

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200


class MarkerLimit(object):
    @staticmethod
    def get_marker_and_limit(req):
        """
        :param req:
        :return: marker, limit, err. if marker or limits are not int returns an err
        """
        marker, limit, err = 0, 0, None
        try:
            marker = int(req.params.get('marker', 0))
            try:
                limit = int(req.params.get('limit', API_DEFAULT_LIMIT))
            except ValueError:
                err = "limit must be an integer number."
        except ValueError:
            err = "marker must be an integer number."
        return marker, limit, err


class TodosHandler(MarkerLimit):

    def __init__(self, db):
        self.db = db

    def on_get(self, req, resp):
        marker, limit, err = self.get_marker_and_limit(req)
        if err is None:
            todos = self.db.get_todos(marker, limit)
            resp.set_header('Content-Type', 'application/json')
            resp.body = json.dumps(todos, sort_keys=False)
            resp.status = falcon.HTTP_200
        else:
            resp.body = err
            resp.status = falcon.HTTP_400

    def on_post(self, req, resp):
        try:
            body = json.loads(req.req_body)
            data = self.db.add_todo(body)
            resp.set_header('Content-Type', 'application/json')
            ret = {'id': data['id'], 'title': data['title'], 'status': data['status']}
            resp.body = json.dumps(ret, sort_keys=False)
            resp.status = falcon.HTTP_201
        except (ValueError, json.decoder.JSONDecodeError):
            resp.status = falcon.HTTP_400
            resp.body = 'Malformed JSON. Could not decode the request body. The JSON was incorrect.'


class TodoHandler(object):

    def __init__(self, db):
        self.db = db

    def on_put(self, req, resp, todo_id):
        try:
            todo = json.loads(req.req_body)
            found, todo = self.db.put_todo(todo_id, todo)
            if found:
                resp.set_header('Content-Type', 'application/json')
                resp.body = json.dumps(todo, sort_keys=False)
                resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_404
        except (ValueError, json.decoder.JSONDecodeError):
            resp.status = falcon.HTTP_400
            resp.body = 'Malformed JSON. Could not decode the request body. The JSON was incorrect.'

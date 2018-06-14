import json
import os

import falcon
import psycopg2
import psycopg2.extras


class HealthHandler(object):

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200


class TodosHandler(object):

    def on_get(self, req, resp):
        conn = psycopg2.connect(host=os.environ["DB_HOST"],
                                dbname=os.environ["DB_NAME"],
                                user=os.environ["DB_USER"],
                                password=os.environ["DB_PASSWORD"])
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM public.todo")
        todos = cur.fetchall()
        cur.close()
        conn.close()
        resp.set_header('Content-Type', 'application/json')
        resp.body = json.dumps(todos, sort_keys=False)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        body = json.loads(req.req_body)
        conn = psycopg2.connect(host=os.environ["DB_HOST"],
                                dbname=os.environ["DB_NAME"],
                                user=os.environ["DB_USER"],
                                password=os.environ["DB_PASSWORD"])
        cur = conn.cursor()
        cur.execute("INSERT INTO public.todo (title, status) VALUES ('{}', '{}')"
            .format(body['title'], body['status']))
        conn.commit()
        cur.close()
        conn.close()
        resp.status = falcon.HTTP_200


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

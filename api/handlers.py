import json
import os

import falcon
import psycopg2
import psycopg2.extras

from json import JSONDecodeError


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

    def on_put(self, req, resp, todo_id):
        """
        Complete update of a record.
        """
        try:
            # Deserialize the request and validate the keys
            body = json.loads(req.req_body)
            for key in {'title', 'status'}:
                if key not in body:
                    raise ValueError
            if len(body.keys()) != 2:
                raise ValueError
        except (JSONDecodeError, ValueError):
            resp.status = falcon.HTTP_400
            return
        try:
            # Try parse the todo id
            todo_id = int(todo_id)
        except ValueError:
            resp.status = falcon.HTTP_400
            return
        conn = psycopg2.connect(host=os.environ["DB_HOST"],
                                dbname=os.environ["DB_NAME"],
                                user=os.environ["DB_USER"],
                                password=os.environ["DB_PASSWORD"])
        cur = conn.cursor()
        cur.execute("UPDATE public.todo SET title=%s, status=%s WHERE id=%s",
                    (body['title'], body['status'], todo_id))
        if cur.rowcount == 1:
            conn.commit()
            resp.set_header('Content-Type', 'application/json')
            # No need to query the database again on success
            resp.body = json.dumps({
                'id': todo_id,
                'title': body['title'],
                'status': body['status'],
            })
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404
        cur.close()
        conn.close()

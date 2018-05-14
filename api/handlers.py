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

    def on_put(self, req, resp, todo_id):
        # Check that todo_id is an int
        try:
            int(todo_id)
        except ValueError:
            resp.status = falcon.HTTP_400
            return

        body = json.loads(req.req_body)
        # Check that either 'title' or 'status' are in the body
        if 'title' not in body and 'status' not in body:
            resp.status = falcon.HTTP_400
            return

        conn = psycopg2.connect(host=os.environ["DB_HOST"],
                                dbname=os.environ["DB_NAME"],
                                user=os.environ["DB_USER"],
                                password=os.environ["DB_PASSWORD"])
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        # Construct an UPDATE statement according to what column data is in the body,
        # since updating a todo item usually doesn't require updating the title.
        cur.execute("UPDATE public.todo SET {} WHERE id = '{}' RETURNING *"
                    .format(", ".join('{} = \'{}\''.format(i[0], i[1]) for i in body.items()),
                            todo_id))
        updated_todo = cur.fetchall()
        if len(updated_todo) is 0:
            cur.close()
            conn.close()
            resp.status = falcon.HTTP_400
            return
        conn.commit()
        cur.close()
        conn.close()
        resp.set_header('Content-Type', 'application/json')
        resp.body = json.dumps(updated_todo, sort_keys=False)
        resp.status = falcon.HTTP_200

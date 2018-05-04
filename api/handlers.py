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

    def on_put(self,req,resp,todoID=''):
        body = json.loads(req.req_body)
        if 'title' not in body or 'status' not in body or body == None:
            resp.body = json.dumps({u'ERROR':'request does not have a title or status'}, sort_keys=False)
            resp.status = falcon.HTTP_404
        elif not todoID.isdigit():
            resp.body = json.dumps({u'ERROR':'todoID is not correct'}, sort_keys=False)
            resp.status = falcon.HTTP_404
        else:
            conn = psycopg2.connect(host=os.environ["DB_HOST"],
                                    dbname=os.environ["DB_NAME"],
                                    user=os.environ["DB_USER"],
                                    password=os.environ["DB_PASSWORD"])
            cur = conn.cursor()
            cur.execute("Update public.todo set title = '{}' , status = '{}' where id = {}"\
                .format(body['title'], body['status'],todoID))
            if cur.rowcount == 1:
                conn.commit()
                cur.execute("SELECT status FROM public.todo where id = {}".format(todoID))
                todos = cur.fetchall()
                resp.set_header('Content-Type', 'application/json')
                resp.body = json.dumps({'status':todos[0][0]})
            else:
                resp.set_header('Content-Type', 'application/json')
                resp.body = json.dumps({u'ERROR':'todoID not in the database'}, sort_keys=False)
            cur.close()
            conn.close()
            resp.status = falcon.HTTP_200

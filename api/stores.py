import os
import psycopg2
import psycopg2.extras

DB_HOST = os.environ["DB_HOST"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]


class StorageEngine(object):

    def __init__(self):
        """todo: research if this is the right place because this may not be thread safe"""
        self.conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)

    def __del__(self):
        if self.conn is not None:
            self.conn.close()

    def put_todo(self, todo_id, data):
        """
        :param todo_id:
        :param data:
        :return: (boolean, todo)  False, None if todo_id not found in store
                            while True, todo if found
        """
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * from public.todo where id=%s", (todo_id,))
        todo = cur.fetchone()
        cur.close()

        if todo:
            cur = self.conn.cursor()
            cur.execute("UPDATE public.todo SET title = %s, status=%s WHERE id=%s",
                        (data['title'], data['status'], todo_id))
            self.conn.commit()
            cur.close()
            data['id'] = todo_id
            return True, data
        else:
            return False, None

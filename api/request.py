import falcon
import logging
from threading import current_thread
import time
import uuid


log = logging.getLogger(__name__)


class CustomRequest(falcon.Request):
    """
    This custom request object defines variables and functions that make working with Falcon requests a bit more
    convenient for our purposes. Note that it relies on custom middleware to provide values for these variables.
    """

    def __init__(self, env, options=None):
        self.start_time = time.time()
        super().__init__(env)
        self.req_body = None


class RequestMiddleware(object):
    """
    This middleware is required to gather information from the request and transform it to be compatible with our
    custom request class. The logic exists here as middleware to take advantage of Falcon's error handling, which
    does not occur if this logic exists in the custom request constructor.
    """

    def process_request(self, req, resp):
        """
        Used to set up and process our request before it is given to a handler.
        :param req: CustomRequest object
        :param resp: falcon Response object
        :return:
        """
        # Reading the request stream can only be done once (and only for HTTP methods other than GET and DELETE)
        req.req_body = str(req.stream.read(), 'utf-8') if req.method not in ['GET', 'DELETE'] else None


class LoggingMiddleware(object):

    def process_request(self, req, resp):
        """
        Logs an incoming API request
        :param req: CustomRequest object
        :param resp: falcon Response object
        """

        # Create a unique request ID to trace requests through logs
        current_thread().name = uuid.uuid1()
        body = ' '.join(req.req_body.splitlines()) if req.req_body else None
        log.info(u"REQUEST: {} {}|{}|{}".format(req.method, req.path, req.query_string, body))

    def process_response(self, req, resp, resource):
        """
        Logs an outgoing API response
        :param req: CustomRequest object
        :param resp: falcon Response object
        """

        total_time = (time.time() - req.start_time) * 1000
        body = ' '.join(resp.body.splitlines()) if resp.body else None
        log.info(u"RESPONSE: {}|{}|{:.3f}ms".format(resp.status, body, total_time))

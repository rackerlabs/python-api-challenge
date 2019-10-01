import logging

import falcon

from api.handlers import HealthHandler, TodosHandler, TodoHandler
from api.request import CustomRequest, LoggingMiddleware, RequestMiddleware
from api.stores import StorageEngine
from config import settings
from config.settings import config

settings.configure_logging(config.api_logging)

log = logging.getLogger()

db = StorageEngine()

app = falcon.API(request_type=CustomRequest, middleware=[RequestMiddleware(), LoggingMiddleware()])
app.add_route('/health', HealthHandler())
app.add_route('/todos', TodosHandler(db))
app.add_route('/todos/{todo_id:int}', TodoHandler(db))

log.info("Started with config file: {}".format(settings.config_file))

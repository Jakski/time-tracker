import os
import re

import asyncpg
from tornado.web import Application
from tornado.ioloop import IOLoop

from time_tracker import (
    database,
    handlers)


def main():
    pool = IOLoop.current().run_sync(lambda: database.Connection.create_pool())
    app = Application(
        [
            (r'/task\.(.*)', handlers.TaskHandler, {'pool': pool}),
        ],
        debug=bool(os.environ.get('DEBUG', '')))
    app.listen(int(os.environ.get('PORT', '8080')))
    IOLoop.current().start()

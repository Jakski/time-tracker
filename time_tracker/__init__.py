import os

from tornado.web import Application
from tornado.ioloop import IOLoop

from time_tracker import (
    database,
    handlers)


def make_application(pool, debug):
    db_cfg = {'pool': pool}
    return Application(
        [
            (r'/task\.(.*)', handlers.TaskHandler, db_cfg),
            (r'/report', handlers.ReportHandler, db_cfg),
        ],
        debug=debug)


def main():
    pool = IOLoop.current().run_sync(lambda: database.Connection.create_pool())
    app = make_application(pool, bool(os.environ.get('DEBUG', '')))
    app.listen(int(os.environ.get('PORT', '8080')))
    IOLoop.current().start()

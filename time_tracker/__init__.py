import os
import re
from datetime import datetime

import asyncpg
from tornado.web import (
    RequestHandler,
    Application)
from tornado.ioloop import IOLoop

from time_tracker.database import Database


class DatabaseHandlerMixin(RequestHandler):

    def initialize(self, pool):
        self.__pool = pool

    async def prepare(self):
        self.db = await Database(self.__pool)

    def on_finish(self):
        IOLoop.current().add_callback(self.db.release)


class MainHandler(DatabaseHandlerMixin):

    async def post(self):
        await self.db.create_tasks([
            ('Testing', datetime.now(), datetime.now())
        ])


def main():
    pool = IOLoop.current().run_sync(lambda: Database.create_pool(
        os.environ.get('TZ', 'Europe/Warsaw')))
    app = Application(
        [
            (r'/task', MainHandler, dict(pool=pool)),
        ],
        debug=bool(os.environ.get('DEBUG', '')))
    app.listen(int(os.environ.get('PORT', '8080')))
    IOLoop.current().start()

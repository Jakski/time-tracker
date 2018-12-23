from tornado.web import RequestHandler
from tornado.ioloop import IOLoop

from time_tracker import (
    database,
    reports)


class DatabaseMixin(RequestHandler):

    def initialize(self, pool):
        self._pool = pool

    async def prepare(self):
        self.db = await database.Connection(self._pool)

    def on_finish(self):
        IOLoop.current().add_callback(self.db.release)


class TaskHandler(DatabaseMixin):

    async def post(self, extension):
        if extension not in reports.EXTENSIONS:
            self.set_status(400, 'Wrong extension')
            return
        if len(self.request.files.keys()) < 1:
            self.set_status(400, 'No report provided')
            return
        report = getattr(reports, extension.capitalize() + 'Report')
        await self.db.create_tasks(report(
            self.request.files.popitem()[1][0]['body'].decode('utf-8')
        ).parse())

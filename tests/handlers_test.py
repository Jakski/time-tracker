import asyncio
import json
from unittest import TestCase
from unittest.mock import Mock, patch
from datetime import timedelta

from tornado.web import MissingArgumentError

from time_tracker.handlers import ReportHandler, TaskHandler


class TestReportHandler(TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.handler = Mock()
        self.handler.db.get_tag_report.return_value = self.loop.create_future()

    def test_get_tag_report(self):
        tag = 'test'
        interval = timedelta(hours=5)
        self.handler.get_query_argument.return_value = '2018-01-01 00:00'
        self.handler.db.get_tag_report.return_value.set_result(
            [(tag, interval)])
        self.loop.run_until_complete(ReportHandler.get(self.handler))
        self.handler.write.assert_called_with(json.dumps({tag: str(interval)}))

    def test_missing_start(self):
        # Set result to prevent accidental infinite loop
        self.handler.db.get_tag_report.return_value.set_result(None)
        self.handler.get_query_argument.side_effect = MissingArgumentError('')
        self.loop.run_until_complete(ReportHandler.get(self.handler))
        self.handler.set_status.assert_called_with(
            400, 'Missing start or end query parameter')

    def test_malformed_start(self):
        # Set result to prevent accidental infinite loop
        self.handler.db.get_tag_report.return_value.set_result(None)
        self.handler.get_query_argument.return_value = 'Wrong date format'
        self.loop.run_until_complete(ReportHandler.get(self.handler))
        self.handler.set_status.assert_called_with(
            400, 'Query parameters have wrong format')


class TestTaskHandler(TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()
        handler = Mock()
        with open('tests/report.wiki', encoding='utf-8') as report:
            self.report = report.read()
        handler.request.files = {
            'test': (
                {
                    'body': self.report.encode('utf-8')
                },
            )
        }
        self.handler = handler

    @patch('time_tracker.reports.WikiReport')
    def test_create_tasks(self, wiki_report):
        self.handler.db.create_tasks.return_value = self.loop.create_future()
        self.handler.db.create_tasks.return_value.set_result(None)
        self.loop.run_until_complete(TaskHandler.post(self.handler, 'wiki'))
        wiki_report.assert_called_with(self.report)

    def test_missing_report_parser(self):
        self.loop.run_until_complete(TaskHandler.post(
            self.handler, 'wrong_parser'))
        self.handler.set_status.assert_called_with(400, 'Wrong extension')

    def test_missing_report(self):
        self.handler.request.files.popitem()
        self.loop.run_until_complete(TaskHandler.post(self.handler, 'wiki'))
        self.handler.set_status.assert_called_with(400, 'No report provided')

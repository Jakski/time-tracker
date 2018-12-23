from unittest import TestCase
from datetime import datetime

from time_tracker import reports


class TestWikiReport(TestCase):

    @classmethod
    def setUpClass(cls):
        with open('tests/report.wiki', encoding='utf-8') as content:
            cls.content = content.read()
        timestamp_format = '%Y-%m-%d %H:%M'
        cls.parsed = [
            (
                'Thing A',
                ['development', 'programming'],
                datetime.strptime('2018-12-23 01:43', timestamp_format),
                datetime.strptime('2018-12-23 02:00', timestamp_format)
            ),
            (
                'Thing A',
                ['development', 'programming'],
                datetime.strptime('2018-12-23 03:00', timestamp_format),
                datetime.strptime('2018-12-23 04:00', timestamp_format)
            ),
            (
                'Thing B',
                [],
                datetime.strptime('2018-12-23 05:00', timestamp_format),
                datetime.strptime('2018-12-23 06:00', timestamp_format)
            )
        ]

    def test_parsing(self):
        tasks = list(reports.WikiReport(self.content).parse())
        self.assertEqual(self.parsed, tasks)

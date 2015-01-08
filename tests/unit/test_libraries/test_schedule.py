from datetime import datetime
import mock
import unittest

from libraries.schedule import Schedule

class TestSpread(unittest.TestCase):
    def setUp(self):
        self.schedule = Schedule()
        self.year = 2014

    @mock.patch('libraries.schedule.datetime')
    def test_week(self, mock_datetime):
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        mock_datetime.now.return_value = datetime(2014, 12, 28, 9)

        self.assertEqual(self.schedule.week(), 17)

    def test_season_year(self):
        self.assertEqual(self.schedule.season_year(), 2014)

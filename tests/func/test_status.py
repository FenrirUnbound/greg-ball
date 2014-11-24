import main
import unittest
import webtest

class TestStatus(unittest.TestCase):
    def setUp(self):
        self.app = webtest.TestApp(main.application)

    def test_status(self):
        endpoint = '/api/v1/status'

        response = self.app.get(endpoint)
        self.assertEqual(response.status_int, 200)
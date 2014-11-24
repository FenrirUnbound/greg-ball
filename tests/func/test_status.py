import json
import main
import unittest
import webtest
import logging

class TestStatus(unittest.TestCase):
    def setUp(self):
        self.app = webtest.TestApp(main.application)

    def test_status(self):
        endpoint = '/api/v1/status'
        expected_body = {'status': 'OK'}

        response = self.app.get(endpoint)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'application/json')

        data = json.loads(response.body)
        self.assertDictEqual(data, expected_body)
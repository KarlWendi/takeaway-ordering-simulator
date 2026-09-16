import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from fastapi.testclient import TestClient
from streamlit.testing.v1 import AppTest
from api import create_app
from web_client import APIError

class WebsiteTests(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.client = TestClient(create_app(Path(self.directory.name) / 'test.db'))
        self.client.__enter__()
        def request(method, path, **kwargs):
            response = self.client.request(method, path, **kwargs)
            if response.is_error:
                raise APIError(response.json()['detail'])
            return response.json()
        self.mock = patch('web_client.request_api', side_effect=request)
        self.mock.start()
        self.app = AppTest.from_file(str(Path(__file__).with_name('website.py')), default_timeout=20).run()
    def tearDown(self):
        self.mock.stop()
        self.client.__exit__(None, None, None)
        self.directory.cleanup()
    def test_submit_refresh_and_station_changes(self):
        self.assertFalse(self.app.exception)
        self.app.number_input[0].set_value(2)
        self.app.button[1].click().run()
        self.assertFalse(self.app.exception)
        self.assertIn('£7.98', self.app.success[0].value)
        self.assertEqual(self.client.get('/menu').json()[0]['stock'], 18)
        self.app.button[0].click().run()
        self.app.slider[0].set_value(3).run()
        self.assertEqual(len(self.client.get('/orders').json()), 1)
        self.assertEqual(self.client.get('/menu').json()[0]['stock'], 18)
    def test_insufficient_stock_does_not_create_order(self):
        self.app.number_input[0].set_value(21)
        self.app.button[1].click().run()
        self.assertFalse(self.app.exception)
        self.assertEqual(self.app.error[0].value, 'Insufficient stock.')
        self.assertEqual(self.client.get('/orders').json(), [])
        self.assertEqual(self.client.get('/menu').json()[0]['stock'], 20)
    def test_unavailable_service_displays_help(self):
        with patch('web_client.request_api', side_effect=APIError('Service unavailable')):
            app = AppTest.from_file(str(Path(__file__).with_name('website.py'))).run()
        self.assertFalse(app.exception)
        self.assertEqual(app.error[0].value, 'Service unavailable')

if __name__ == '__main__':
    unittest.main()

import unittest
import logging
from threading import Thread

from paloalto_panorama_sdk import PanoramaSDK
from tests.PanoramaAPIMock import panoramaAPIMock


class TestPanoramaSDKService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server_thread = Thread(target=panoramaAPIMock.run_server)
        logging.debug("Starting PanoramaSDKService thread")
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        logging.debug("Stopping PanoramaSDKService thread")
        cls.server_thread.join()

    def setUp(self):
        logging.debug("Starting PanoramaSDKService setUp")
        self.panSDK = PanoramaSDK(url="https://172.17.90.2", username="testuser", password="testpassword")

    def test_panorama_get_apikey(self):
        logging.debug(f"Erwarteter apikey: 'mock_apikey_12345'")
        logging.debug(f"Tatsächlicher apikey: '{self.panSDK.apikey}'")
        self.assertEqual(self.panSDK.apikey, "mock_apikey_12345")


if __name__ == '__main__':
    unittest.main()

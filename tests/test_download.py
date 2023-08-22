import unittest
from luseFinReportDownloader import download
class TestConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.custom_config = download.Config(start=(2005, 9, 22), end=(3091, 9, 22))
        self.default_config = download.Config()
    def test_get_starturl_from_custom_config(self):
        self.assertEqual(self.custom_config.get_start(), (False, '2005-September-22-Trade-Summary.pdf'))

if __name__ == '__main__':
    unittest.main()
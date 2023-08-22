import unittest
from luseFinReportDownloader import download
class TestConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.custom_config = download.Config(start=(2021, 10, 4), end=(2022, 3, 22))
        self.default_config = download.Config()
    def test_get_starturl_from_custom_config(self):
        self.assertEqual(self.custom_config.get_start(), (False, '04-October-2021-Trade-Summary-Report.pdf'))
    def test_get_endurl_from_custom_config(self):
        self.assertEqual(self.custom_config.get_end(), (False, '22-March-2022-Trade-Summary-Report.pdf'))
    def test_get_endurl_from_default_config(self):
        self.assertEqual(self.default_config.get_end(), (True, ""))
    def test_get_starturl_from_default_config(self):
        self.assertEqual(self.default_config.get_start(), (True, ""))

if __name__ == '__main__':
    unittest.main()
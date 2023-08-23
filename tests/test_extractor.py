import unittest
from luseFinReportDownloader import extract
from luseFinReportDownloader.download import Config
class ExtractorTest(unittest.TestCase):

    def setUp(self):
        config = Config(start=(2021, 10, 29), end=(2021, 10, 22))
        self.extractor = extract.DocumentExtractor(config=config)
    def test_getstreams(self):
        self.assertEqual(len(self.extractor.streams), 5)
    def test_get_dataframes(self):
        dfs = self.extractor.generate_dataframes()
        columns = dfs[0][1].columns
        print(columns)
        for df in dfs:
            self.assertEqual(columns, df[1].columns)
if __name__ == '__main__':
    unittest.main()
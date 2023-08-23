import io
from luseFinReportDownloader import download
from luseFinReportDownloader import read_data
import pandas as pd
import tempfile
from luseFinReportDownloader.download import Config

class DocumentExtractor:
    def __init__(self, config=Config):
        downloader = download.Downloader(config=config)
        downloader.fetch_streams()
        self.streams = downloader.streams

    def generate_dataframes(self):
        dataframes = []
        for idx, stream in enumerate(self.streams):
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf_file:
                temp_pdf_file.write(stream['data'].getvalue())
                src_pdf = temp_pdf_file.name
                dataframes.append({'text': stream['text'], 'df': read_data.get_data(src_pdf)})
            
            '''
            output_filename = f"output_data_{idx}.csv"
            dataframe.to_csv(output_filename, index=False)
            '''
            temp_pdf_file.close()
        return dataframes
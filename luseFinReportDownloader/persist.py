from luseFinReportDownloader import extract
from luseFinReportDownloader import download

class Persist:
    def __init__(self, dfs):
        self.dfs = dfs
    def to_csv(self):
        for df in self.dfs:
            df['df'].to_csv(f"{df['text']}.csv", index=False)
    def to_json(self):
        for df in self.dfs:
            df['df'].to_excel(f"{df['text']}.xlsx", index=False)
    def to_pickle(self):
        for df in self.dfs:
            df['df'].to_pickle(f"{df['text']}.pkl")
    def to_json(self):
        for df in self.dfs:
            df['df'].to_json(f"{df['text']}.json", orient='records')
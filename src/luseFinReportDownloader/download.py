import io
import enum
import requests
from bs4 import BeautifulSoup

class Month(enum.Enum):
	JANUARY = 1
	FEBRUARY = 2
	MARCH = 3
	APRIL = 4
	MAY = 5
	JUNE = 6
	JULY = 7
	AUGUST = 8
	SEPTEMBER = 9
	OCTOBER = 10
	NOVEMBER = 11
	DECEMBER = 12

class Config:
	url = "https://luse.co.zm/market-data/"
	el_class = "download-link"
	single_download = False # if set to True will only download the start data
	start = (0,0,0) # This makes the script download all the data (0,0,0) rpresents (year, month, day)
	# (-1, -1, -1) This makes the model download all the data
	# uses same representation as start
	# Only considered when single_download=False
	end = (-1,-1,-1)
	def __init__(self, url=None, el_class=None, single_download=None, start=None, end=None):
		if url != None:
			self.url = url
		if el_class != None:
			self.el_class = el_class
		if single_download != None:
			self.single_download = single_download
		if start != None:
			self.start = start
		if end != None:
			self.end = end
	# Returns (bool, str)
	# Where;
	# if bool is true then start is the first link
	# str is a representation of the date eg 22_September_2005
	def get_start(self) -> (bool, str):
		if [True, True, True] == [d == 0 for d in self.start]:
			return (True, "")
		else:
			# (year, month, day)
			# interpret the month
			m = Month(self.start[1]).name
			day = f"0{self.start[2]}" if self.start[2] < 10 else f"{self.start[2]}"
			return (False, f"{day}-{m.capitalize()}-{self.start[0]}-Trade-Summary-Report.pdf")
	# Returns (bool, str)
	# Where;
	# if bool is true then end we run until the last link
	# str is a representation of the date eg 22-September-2005
	def get_end(self) -> (bool, str):
		if [True, True, True] == [d == -1 for d in self.end]:
			return (True, "")
		else:
			# (year, month, day)
			# interpret the month
			m = Month(self.end[1]).name
			day = f"0{self.end[2]}" if self.end[2] < 10 else f"{self.end[2]}"
			return (False, f"{day}-{m.capitalize()}-{self.end[0]}-Trade-Summary-Report.pdf")
class Downloader:
	def __init__(self, config=Config):
		self.config = config
		self.streams = []
		self.urls = []
		self.initialize()
		self.fetch_links()
		print("Downloader process started")
		print(f"Downloader configuration:\n{config.__dict__}")
	def initialize(self) -> (bool, io.BytesIO):
		self.response = requests.get(self.config.url)
		if self.response.status_code != 200:
			raise Exception(f"Error fetching base url returned status_code {self.response.status_code}")
		self.soup = BeautifulSoup(self.response.content, 'html.parser')
	def fetch_data(self, url, stream=True):
		res = requests.get(url, stream=stream)
		if res.status_code == 200:
			f_stream = io.BytesIO()
			for chunk in res.iter_content(chunk_size=8192):
				f_stream.write(chunk)
			f_stream.seek(0)
			return (True, f_stream)
		else:
			return (False, io.BytesIO)
	def fetch_links(self):
		for link in self.soup.find_all('a', class_=self.config.el_class):
			try:
				text = link.get_text().split()[0]
				self.urls.append({'text': text, 'url': link['href']})
			except:
				pass
	def get_start_idx(self):
		if self.config.get_start() == (True, ""):
			return 0
		for idx, link in enumerate(self.urls):
			if link['text'] == self.config.get_start()[1]:
				return idx
	def get_end_idx(self):
		if self.config.get_end() == (True, ""):
			return len(self.urls) - 1
		for idx, link in enumerate(self.urls):
			print(link)
			if link['text'] == self.config.get_end()[1]:
				return idx
	def fetch_streams(self):
		new_urls = self.url[self.get_start_idx(): self.get_end_idx() + 1]
		for url in new_urls:
			success, data = self.fetch_data(url['url'])
			if success:
				self.streams.append(data)
			else:
				print("Error saving stream")
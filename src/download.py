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
		self.set_value(self.url, url)
		self.set_value(self.el_class, el_class)
		self.set_value(self.single_download, single_download)
		self.set_value(self.start, start)
		self.set_value(self.end, end)
	def set_value(self, a, b):
		a = b if b != None else a
	# Returns (bool, str)
	# Where;
	# if bool is true then start is the first link
	# str is a representation of the date eg 22_September_2005
	def get_start(self) -> (bool, str):
		if [d == 0 for d in self.start]:
			return (True, "")
		else:
			# (year, month, day)
			# interpret the month
			m = Month(self.start[1]).name
			return (False, f"{self.start[0]}-{m.capitalize}-{self.start[2]}")
	# Returns (bool, str)
	# Where;
	# if bool is true then end we run until the last link
	# str is a representation of the date eg 22-September-2005
	def get_end(self) -> (bool, str):
		if [d == -1 for d in self.end]:
			return (True, "")
		else:
			# (year, month, day)
			# interpret the month
			m = Month(self.end[1]).name
			return (False, f"{self.end[0]}-{m.capitalize}-{self.end[2]}")
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
			self.urls.append(link['href'])
	def fetch_streams(self):
		for url in self.urls:
			success, data = self.fetch_data(url)
			if success:
				self.streams.append(data)
			else:
				print("Error saving stream")
import io
import re
import PyPDF2
import tempfile
import requests
from lisa.models import (create_document, generate_dict)
from bs4 import BeautifulSoup

def get_data(pdf_src: str) -> (bool, list, str, str):
	m_i = {"January": "01","February": "02","March": "03","April": "04","May": "05","June": "06","July": "07","August": "08","September": "09","October": "10","November": "11","December": "12"}
	try:
		reader = PyPDF2.PdfReader(pdf_src)
		page = reader.pages[0]
		text = page.extract_text().split("\n")
		start_idx = 0
		date = ''
		for i in range(len(text)):
			if text[i].strip() == "Sells":
				start_idx = i
				break
		for line in text:
			if 'trade summary report' in line.lower():
				print(line)
				date_lst = line.split()[-3:]
				date = f"{date_lst[2]}-{m_i[date_lst[1]]}-{date_lst[0]}"
				print(date)
		new_list = text[start_idx+1:]
		stock = []
		for a in new_list:
			if a == '' or a.isspace():
				pass
			else:
				lst = a.split().insert(0, date)
				stock.append(a.split())

		for s in stock:
			if len(s) < 20:
				raise Exception("Error Less than 20")
		return (True, stock, date, '')
	except Exception as e:
		return (False, [], '', str(e))

res = requests.get("https://luse.co.zm/market-data/")
if res.status_code != 200:
	raise Exception("Error fetching data")
soup = BeautifulSoup(res.content, "html.parser")
pdf_links = soup.find_all('a', href=re.compile(r'\.pdf$'))
links = [link["href"] for link in pdf_links]
links = links[:3]
data = []
for link in links:
	res = requests.get(link, stream=True)
	if res.status_code == 200:
		f_stream = io.BytesIO()
		for chunk in res.iter_content(chunk_size=8192):
			f_stream.write(chunk)
		f_stream.seek(0)
		data.append(f_stream)
stocks = []
for d in data:
	with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
		temp_file.write(d.getvalue())
		src = temp_file.name
		stock_data = get_data(src)
		stocks.append(stock_data)
		temp_file.close()

for s in stocks:
	for stock_data in s[1]:
		create_document(generate_dict(
	        date = s[2],
	        instrument = stock_data[0],
	        bid_qty = stock_data[1],
	        bid_price = stock_data[2],
	        ask_price = stock_data[3],
	        ask_qty = stock_data[4],
	        last_trade_price = stock_data[5],
	        net_change = stock_data[6],
	        closing_price = stock_data[7],
	        total_turnover = stock_data[8],
	        average_price = stock_data[9],
	        last_traded_size = stock_data[10],
	        week_52_high = stock_data[11],
	        week_52_low = stock_data[12],
	        opening_price = stock_data[13],
	        change = stock_data[14],
	        previous_closing_price = stock_data[15],
	        total_trades = stock_data[16],
	        trade_volume = stock_data[17],
	        foreign_buys = stock_data[18],
	        foreign_sells = stock_data[19],
    	)
	)

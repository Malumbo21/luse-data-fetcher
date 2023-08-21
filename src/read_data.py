import tabula
import pandas as pd

class Config:
	pages = 1
	relative_area = True
	relative_columns = True
	area = [30, 0, 894, 400]

def get_data(src_pdf, config = Config) -> (bool, pd.DataFrame, str):
	data = tabula.read_pdf(src_pdf, pages=config.pages, relative_area=config.relative_area, relative_columns=config.relative_columns, area=config.area)
	try:
		df = data[0]
		columns = df.columns
		df.fillna("nan", inplace=True)
		r1 = df.drop(df.index[0], inplace=True)
		r2 = df.drop(df.index[0], inplace=True)
		filtered_columns = []
		i = 0
		for c in columns:
			column = ""
			column += c
			if r1[i] != "nan":
				column += " " + r1[i]
			if r2[i] != "nan":
				column += " " + r2[i]
			i += 1
			filtered_columns.append(column)
		df.drop(df.index[-1], inplace=True)
		df.columns = filtered_columns
		return (True, df, "")
	except:
		return (False, pd.DataFrame, "Error list index out of range")
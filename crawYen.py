#encoding: UTF-8
import sys
import urllib.request
import urllib
from bs4 import BeautifulSoup
import csv

def main():
	yearStart = 2015
	while yearStart<=2015:
		fetchOneYear(yearStart)
		yearStart = yearStart+1

def fetchOneYear(year):
	url = "http://app.finance.ifeng.com/hq/rmb/quote.php?symbol=JPY&begin_day=%s-01-01&end_day=%s-01-01"
	url = url % (year, year+1)
	response = urllib.request.urlopen(url)
	html = BeautifulSoup(response.read().decode('utf-8'))
	fileName = "jpy%s-%s.csv" % (year,year+1)
	print("writing: ", fileName)
	with open(fileName, 'w') as csvfile:
		fieldnames = ['日期', '中间价','钞买价','汇买价','钞/汇卖价','涨跌额','涨跌幅']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		parseExchangeData(writer, html)
 

def parseExchangeData(writer, data):
	for table in data.find_all('table'):        
		for row in table.find_all('tr'):
			variants = {}
			i=0
			for tr in row.find_all('td'):
				title=getTitle(i)
				i=i+1
				value = tr.text.replace(u'\xa0',u'')
				value = value.replace(u'\xc2',u'')
				variants[title]=value
			if i!=0:
				writer.writerow(variants)

def getTitle(idx):  
	if idx==0:      
		return '日期'
	elif idx==1:       
		return '中间价'
	elif idx==2:
		return '钞买价'
	elif idx==3:
		return '汇买价'
	elif idx==4:
		return '钞/汇卖价'
	elif idx==5:
		return '涨跌额'
	else:
		return '涨跌幅'
  

if __name__ == '__main__':
    print("running...")
    main()
    print("Finshed!")

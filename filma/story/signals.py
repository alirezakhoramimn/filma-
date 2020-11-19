import json
from bs4 import BeautifulSoup
import requests


def doing():
	d = requests.get("http://dl4.golchinup.ir/new/Serial/")
	soup = BeautifulSoup(d.text, features="lxml")
	for ln in soup.find_all('td', attrs={'class':'link'}):
		name_of_series = ln.a.text
		skip = 'Parent directory/'
		if name_of_series != skip:
			print(name_of_series)
			s = requests.get(f'http://dl4.golchinup.ir/new/Serial/{name_of_series}')
			soup = BeautifulSoup(s.text, features="lxml")
			for ln2 in soup.find_all('td', attrs={'class':'link'}):
				season = ln2.a.text
				if season != skip:

					print(season)
					s = requests.get(f'http://dl4.golchinup.ir/new/Serial/{name_of_series}{season}')
					soup = BeautifulSoup(s.text, features="lxml")
					is_dubbed = requests.get(f'http://dl4.golchinup.ir/new/Serial/{name_of_series}{season}DUBLE')

					if is_dubbed.ok:
						for ln3 in soup.find_all('td', attrs={'class':'link'}):
							res = ln3.a.text
							
							if res != skip:
								print(res)									
								s = requests.get(f'http://dl4.golchinup.ir/new/Serial/{name_of_series}{season}DUBLE/{res}')
								soup = BeautifulSoup(s.text, features="lxml")
								
								for ln4 in soup.find_all('td', attrs={'class':'link'}):
									no = ln4.a.text
									
									if no != skip:
										print(no)
										with open('key.json', 'a+') as file:
											d = {'name_of_series':name_of_series[:-1],'season':season[:-1],'res':res[:-1],'num':no[-1]}
											d = json.dumps(d)
											file.write(d)
					else:
						for ln3 in soup.find_all('td', attrs={'class':'link'}):
							res = ln3.a.text
							
							if res != skip:
								print(res)									
								s = requests.get(f'http://dl4.golchinup.ir/new/Serial/{name_of_series}{season}{res}')
								soup = BeautifulSoup(s.text, features="lxml")
								
								for ln4 in soup.find_all('td', attrs={'class':'link'}):
									no = ln4.a.text
									
									if no != skip:
										print(no)
										with open('key.json', 'a+') as file:
											d = {'name_of_series':name_of_series[:-1],'season':season[:-1],'res':res[:-1],'num':no[-1]}
											d = json.dumps(d)
											file.write(d)



doing()
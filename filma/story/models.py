from django.db import models
from hashlib import sha256 
from django.core.validators import URLValidator 
from django.core.exceptions import ValidationError
from graphql import GraphQLError 
import re 
import json
from bs4 import BeautifulSoup
import requests

class Initials(models.Model):
	initial = models.CharField(max_length=3)

class Name(models.Model):
	name = models.CharField(max_length=50,blank=True, null=True, default='2')
	initial = models.ForeignKey(Initials, on_delete = models.CASCADE, related_name='names')


class Season(models.Model):
	num = models.CharField(max_length=5,blank=True, null=True)
	name = models.ForeignKey(Name, on_delete=models.CASCADE)	
	

class Resolution(models.Model):


	res = models.CharField(max_length=600)

#	name = models.ForeignKey(Name, on_delete=models.CASCADE)	
	season = models.ForeignKey(Season, on_delete=models.CASCADE)

class Film(models.Model):
	az = models.URLField(blank=True, null=True)
	full = models.URLField(unique=True,blank=True, null=True)
	hashed_full = models.URLField(unique=True,blank=True, null=True)
	click_times = models.IntegerField(default=1,blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)


	# Now let us count the click times and actually use the hash stuff 
	def clicking(self):
		self.click_times += 1
		self.save()



	def save(self,*args,**kwargs):
		if not self.id:
			# we would like to have the hexdigested hash to 8 chars. 
			# we don't need to overcomplicate this crap

			self.hashed_full = sha256(self.full.encode()).hexdigest()[:8]
		

		validation = URLValidator()
		try:
			validation(self.full)

		except ValidationError as error:
			raise GraphQLError('دوتس عزیز لطفا لینک درست رو قرار بده!!!')
		
		return super().save(*args, **kwargs)

	class Meta:
		abstract = True 



class Series(Film):
	res = models.ForeignKey(Resolution, on_delete=models.CASCADE)	
	# season = models.ForeignKey(Season, on_delete=models.CASCADE)
	no = models.TextField()



	def __str__(self):
		return self.hashed_full 



def series_scraper():
	url = 'http://dls1.mydownloadcenter.pw/Series/'
	d = requests.get(url)
	
	soup = BeautifulSoup(d.text, features='lxml')
	skip = 'Parent directory/'
		
	for ln in soup.find_all('td', attrs={'class':'n'}):
		if ln.a.text != skip:
			init = Initials.objects.create(initial=ln.a.text)
			soup = BeautifulSoup(requests.get(f'{url}{ln.a.text}/').text, features='lxml')
			for ln1 in soup.find_all('td', attrs={'class':'n'}):
				if ln1.a.text != skip:
					name = Name.objects.create(name=ln1.a.text,initial= init)
					soup = BeautifulSoup(requests.get(f'{url}{ln.a.text}/{ln1.a.text}/').text, features='lxml')
					for ln2 in soup.find_all('td', attrs={'class':'n'}):
						if ln2.a.text != skip:
							season = Season.objects.create(name=name, num = ln2.a.text)
							soup = BeautifulSoup(requests.get(f'{url}{ln.a.text}/{ln1.a.text}/{ln2.a.text}/').text, features='lxml')
							for ln3 in soup.find_all('td', attrs={'class':'n'}):
								if ln3.a.text != skip:
									x = re.find_all('x...', ln3.a.text)
									#ln3.a.text[:5]
									if x:
										res = f'{ln3.a.text[:5]}{x[0]}'
									else:
										res = ln3.a.text[:5]
									
									reso = Resolution.objects.create(season=season, res = res)
									soup = BeautifulSoup(requests.get(f'{url}{ln.a.text}/{ln1.a.text}/{ln2.a.text}/{ln3.a.text}/').text, features='lxml')

									for ln4 in soup.find_all('td', attrs={'class':'n'}):
										if ln4.a.text != skip:
											Series.objects.create(res=reso, az=url,no=ln4.a.text, full=f'{url}{ln.a.text}/{ln1.a.text}/{ln2.a.text}/{ln3.a.text}/{ln4.a.text}', )	
											#dic = {'startes':ln.a.text, 'name':ln1.a.text,'season':ln2.a.text,'res':res, 'series':f'{url}{ln.a.text}/{ln1.a.text}/{ln2.a.text}/{ln3.a.text}/{ln4.a.text}'}
											#with open('links.json', 'a+') as file:
											#	json.dump(dic, file)	


series_scraper()



def do():
	from bs4 import BeautifulSoup 
	import requests as r 
	#for x in range(8,11):
	d = r.get(f'http://dl4.golchinup.ir/new/Serial/')
	soup = BeautifulSoup(d.text)
	for ln in soup.find_all('td', attrs={"class":'link'}):
		#	print(ln.a.text[:-1])
		name = ln.a.text
		#name_obj = Name.objects.create(name=name[-1])
		d = r.get(f'http://dl4.golchinup.ir/new/Serial/{name}')
		soup = BeautifulSoup(d.text)
		for ln in soup.find_all('tr'):
			season = ln.a.text
			#ses_obj = Season.objects.create(num=season[:-1])

			d = r.get(f'http://dl4.golchinup.ir/new/Serial/{name}{season}')
			soup = BeautifulSoup(d.text)
			for ln in soup.find_all('td', attrs={'class':'link'}):
				reso = ln.a.text
				#Resolution.objects.create(res=reso)

#do()


'''
def do():
	from bs4 import BeautifulSoup 
	import requests as r 
	#for x in range(8,11):
	d = r.get(f'http://dls.megauploads.ir/DonyayeSerial/series/')
	soup = BeautifulSoup(d.text)
	for ln in soup.find_all('td', attrs={"class":'link'}):
		Name.objects.create(name=ln.a.text)
		s = r.get(f'http://dl4.golchinup.ir/new/Serial/{ln.a.text}')
		souper = BeautifulSoup(s.text)
		for ln in souper.find_all('td', attrs={'class':'link'}):
			season = ln.a.text[:-1]
			s = r.get(f'http://dl4.golchinup.ir/new/Serial/{ln.a.text}{season}')
			souper = BeautifulSoup(s.text)
			for q in soup.find_all('td', attrs={'class':'link'}):
				print(q.a.text)

'''


class Movie(Film):
	name = models.CharField(max_length=100,blank=True, null=True)

	def __str__(self):
		return self.name 


		
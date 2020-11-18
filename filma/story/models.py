from django.db import models
from hashlib import sha256 
from django.core.validators import URLValidator 
from django.core.exceptions import ValidationError
from graphql import GraphQLError 
from multiselectfield import MultiSelectField

# Create your models here.



class Name(models.Model):
	name = models.CharField(max_length=50,blank=True, null=True)


class Season(models.Model):
	num = models.CharField(max_length=5,blank=True, null=True)


class Resolution(models.Model):
	CHOICES = (
		('720p', '720p'),
		('1080', '1080p'),
		('720p', '480p'),
		('360p', '360p'),

	)

	res  = MultiSelectField(CHOICES, default='480p')
	



class Film(models.Model):
	az = models.URLField(blank=True, null=True)
	res = models.ForeignKey(Resolution, on_delete=models.CASCADE)
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
	name = models.ForeignKey(Name, on_delete=models.CASCADE)	
	season = models.ForeignKey(Season, on_delete=models.CASCADE)




	def __str__(self):
		return self.hashed_full 


def do():
	from bs4 import BeautifulSoup 
	import requests as r 
	#for x in range(8,11):
	d = r.get(f'http://dl4.golchinup.ir/new/Serial/')
	soup = BeautifulSoup(d.text)
	for ln in soup.find_all('td', attrs={"class":'link'}):
		#	print(ln.a.text[:-1])
		name = ln.a.text
		name_obj = Name.objects.create(name=name[-1])
		d = r.get(f'http://dl4.golchinup.ir/new/Serial/{name}')
		soup = BeautifulSoup(d.text)
		for ln in soup.find_all('td', attrs={'class':'link'}):
			season = ln.a.text
			ses_obj = Season.objects.create(num=season[:-1])

			d = r.get(f'http://dl4.golchinup.ir/new/Serial/{name}{season}')
			soup = BeautifulSoup(d.text)
			for ln in soup.find_all('td', attrs={'class':'link'}):
				series = ln.a.text
				Series.objects.create(name=name_obj, season=ses_obj,full=f'http://dl4.golchinup.ir/new/Serial/{name}{season}{series}')




'''
def do():
...     from bs4 import BeautifulSoup 
...     import requests as r 
...     #for x in range(8,11):
...     d = r.get(f'http://dls.megauploads.ir/DonyayeSerial/series/')
...     soup = BeautifulSoup(d.text)
...     for ln in soup.find_all('td', attrs={"class":'link'}):
...             #       print(ln.a.text[:-1])
...             Name.objects.create(name=ln.a.text)
...             s = r.get(f'http://dl4.golchinup.ir/new/Serial/{ln.a.text}')
...             souper = BeautifulSoup(s.text)
...         	for ln in souper.find_all('td', attrs={'class':'link'}):
...                     season = ln.a.text[:-1]
...                     s = r.get(f'http://dl4.golchinup.ir/new/Serial/{ln.a.text}{season}')
...                     souper = BeautifulSoup(s.text)
...                     for q in soup.find_all('td', attrs={'class':'link'}):
...                             print(q.a.text)
... 

'''
class Movie(Film):
	name = models.CharField(max_length=100,blank=True, null=True)

	def __str__(self):
		return self.name 
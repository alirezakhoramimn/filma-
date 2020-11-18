from django.db import models
from hashlib import sha256 
from django.core.validators import URLValidator 
from django.core.exceptions import ValidationError
from graphql import GraphQLError 
# Create your models here.



class Name(models.Model):
	name = models.CharField(max_length=50,blank=True, null=True)


class Season(models.Model):
	num = models.IntegerField(blank=True, null=True)



class Film(models.Model):
	bio = models.TextField()
	released_date = models.DateTimeField(auto_now=False,blank=True, null=True)
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
	name = models.ForeignKey(Name, on_delete=models.CASCADE)	
	season = models.ForeignKey(Season, on_delete=models.CASCADE)




	def __str__(self):
		return self.url 

'''
def do():
	from bs4 import BeautifulSoup 
	import requests as r 
	#for x in range(8,11):
	d = r.get(f'http://dls.megauploads.ir/DonyayeSerial/series/')
	soup = BeautifulSoup(d.text)
	for ln in soup.find_all('tr'):
		Name.objects.create(name=ln.a.text)
#do()
'''
class Movie(Film):
	name = models.CharField(max_length=100,blank=True, null=True)

	def __str__(self):
		return self.name 
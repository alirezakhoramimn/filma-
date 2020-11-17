from django.db import models
from hashlib import sha256 
# Create your models here.

class Name(models.Model):
	name = models.CharField(max_length=50)

class Movie(models.Model):
	name = models.ForeignKey(Name, on_delete=models.CASCADE)
	bio = models.TextField()
	link = models.URLField(blank=True, null=True)

def do():
	from bs4 import BeautifulSoup 
	import requests as r 
	#for x in range(8,11):
	d = r.get(f'http://dls.megauploads.ir/DonyayeSerial/series/')
	soup = BeautifulSoup(d.text)
	for ln in soup.find_all('tr'):
		Name.objects.create(name=ln.a.text)
#do()


from .models import Name, Movie 

from bs4 import BeautifulSoup 
import requests as r 
s = []
#for x in range(8,11):
d = r.get(f'http://dls.megauploads.ir/DonyayeSerial/series/')
soup = BeautifulSoup(d.text)
for ln in soup.find_all('tr'):
  Name.objects.create(name={ln.a.text})
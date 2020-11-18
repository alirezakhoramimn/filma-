from django.shortcuts import render, get_list_or_404
from django.views.generic import ListView, DetailView
from .models import Movie, Name, Series, Resolution
# Create your views here.=

def index(request):
	qs = Name.objects.all()
	ls = Movie.objects.all()
	s = Series.objects.all()
	r = Resolution.objects.all()

	return render(request, 'story/list.html', {"names":qs, 'res':r, 'series':s,'movie':ls})


def detail(request, name):
	qs = get_object_or_404(Movie, name=name)
	return render(request, 'movie/detail.html', {'movies':qs})







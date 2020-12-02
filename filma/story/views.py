from django.shortcuts import render, get_list_or_404, get_object_or_404
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
	init = name[0]
	qs = get_object_or_404(Name, initial=init)
	return render(request, 'movie/detail.html', {'movies':qs})







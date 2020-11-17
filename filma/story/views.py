from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Movie, Name
# Create your views here.=

def index(request):
	qs = get_object_or_404(Name)

	return render(request, 'movie/list.html', {"names":qs})


def detail(request, name):
	qs = get_object_or_404(Movie, name=name)
	return render(request, 'movie/detail.html', {'movies':qs})







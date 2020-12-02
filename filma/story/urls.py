from django.urls import path
from . import views 

app_name = 'story'
urlpatterns = [
	path('', views.index, name='index'),
	path('<str:name>', views.detail, name='detail')
]
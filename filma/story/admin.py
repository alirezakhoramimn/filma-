from django.contrib import admin
from .models import Movie, Name, Series, Season, Initials, Resolution
# Register your models here.


admin.site.register(Movie)
admin.site.register(Resolution)
admin.site.register(Initials)
admin.site.register(Name)
admin.site.register(Series)
admin.site.register(Season)


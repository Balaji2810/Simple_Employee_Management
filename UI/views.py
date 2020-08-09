import pytz

from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,"base.html",{"timezone":pytz.all_timezones})

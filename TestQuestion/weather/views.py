from django.shortcuts import render
from django.http import HttpResponse
from weather.weatherAPI import API

# Create your views here.


def index(request):
    table_data =[[]]
    if request.GET:
        if "City" in request.GET:
            table_data = API(request.GET["City"])
        else:
            print(request.GET)
    print(request.GET)

    return render(request,"weather/weather.html",context={"table_data":table_data})
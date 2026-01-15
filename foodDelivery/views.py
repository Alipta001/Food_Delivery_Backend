from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

def home(request:HttpRequest)->HttpResponse:
    if request.method == 'GET':
        msg: str = "Admin DashBoard"
        return render(request,'home.html',{'message':msg})
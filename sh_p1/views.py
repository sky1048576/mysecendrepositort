from django.shortcuts import render,HttpResponse
from persons.models import Picture
# Create your views here.

def index(request,):

        return render(request,"registration/index.html")



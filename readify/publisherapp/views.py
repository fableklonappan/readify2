from urllib import request
from django.shortcuts import redirect, render
from libraryapp.models import RentalRequest
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def logout(request):
    auth.logout(request)
    return redirect('index')

def pubindex(request):
    
    return render(request,'publisher.html')

def s_rent(request):
    user= request.user
    rent_data=RentalRequest.objects.all()
    return render(request,'a_rent.html',{'rent_data': rent_data})
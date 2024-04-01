from urllib import request
from django.shortcuts import redirect, render
from libraryapp.models import AddBook, AudioBook, PdfBook, RentalRequest, paymenthistory, planSubscription
from publisherapp.models import ViewCustomer
from userapp.models import CustomUser, UserProfile
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def logout(request):
    auth.logout(request)
    return redirect('index')

def pubindex(request):
    count_cus = CustomUser.objects.all().count()
    count_book = AddBook.objects.all().count()
    count_audio = AudioBook.objects.all().count()
    count_pdf = PdfBook.objects.all().count()
    count_rent = RentalRequest.objects.filter(request_status='successful').count()
    context ={
        'count_cus':count_cus,
        'count_book':count_book,
        'count_audio':count_audio,
        'count_pdf':count_pdf,
        'count_rent':count_rent,
    }
    return render(request,'publisher/publisher.html' , context= context)

def s_rent(request):
    user= request.user
    rent_data=RentalRequest.objects.all()
    return render(request,'publisher/rent.html',{'rent_data': rent_data})

def viewcust(request):
    view_cus = CustomUser.objects.all()
    context={
        'view_cus':view_cus,
    }
    return render(request,'publisher/viewcustomer.html', context=context)


def detilescust(request, cusid):
    # Retrieve the rental request and user profile objects
    rent_count = RentalRequest.objects.filter(user=cusid).count()
    rent = RentalRequest.objects.filter(user=cusid,request_status='successful')
    sub= planSubscription.objects.filter(user=cusid,status='Active')
    try:
        # Try to get the user profile object related to the given user ID
        user_profile = UserProfile.objects.get(user=cusid)
    except UserProfile.DoesNotExist:
        # If UserProfile.DoesNotExist exception is raised, set user_profile to None
        user_profile = None

    # Pass the objects to the template
    context = {
        'rent_count':rent_count,
        'rent_data': rent,
        'user_profile': user_profile,
        'sub':sub,
    }

    return render(request, 'publisher/more.html', context=context)


def addbook(request):
    return render(request, 'publisher/addbook.html')
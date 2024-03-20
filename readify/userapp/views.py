from datetime import datetime, date
from django.shortcuts import render, redirect
from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout
from django.shortcuts import render, redirect
  
from django.contrib import messages, auth

# In userapp/views.py
from libraryapp.models import BookCart, Wishlist, planSubscription
from .models import UserProfile,CustomUser
# from accounts.backends import EmailBackend
from django.contrib.auth import get_user_model

from django.core.exceptions import ObjectDoesNotExist
User = get_user_model()


from datetime import datetime

def index(request):
    user_id = request.user.id
    books_in_count = BookCart.objects.filter(user_id=user_id).count()
    books_in_countw = Wishlist.objects.filter(user_id=user_id).count()
    current_date = datetime.now().date()
    luffy = 2
    try:
        # Fetch the latest subscription ordered by start date
       sub = planSubscription.objects.order_by('-startdate').filter(user_id=request.user.id).first()
       print (sub)
       if sub:
            luffy= 3
            if sub.payment_status == 'successful':
                if sub.status == 'Active':
                # Check if the subscription is active
                    if sub.enddate.date() > current_date:
                        luffy = 4
    except ObjectDoesNotExist:
        # Handle the case where no subscription exists
        sub = None
    context = {
        'count': books_in_count,
        'countw': books_in_countw,
        'sub': sub,
        'luffy': luffy
    }
    return render(request, "index.html", context=context)







def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pwd')

        if email and password:
            user = authenticate(request, email=email, password=password)
            print("Authenticated user:", user)  # Print the user for debugging
            if user is not None and user.is_active :
                if user.is_active==False:
                        print("Inside user.is_active check")
                        auth_login(request, user)
                        print(user.is_active)
                        error_message = "Inactive login credentials."
                        return render(request, 'login.html', {'error_message': error_message})
                else:
                    if user.is_superuser==1:
                        auth_login(request,user)
                        print(user.role)
                        return redirect('http://127.0.0.1:8000/publisherapp/pubindex/')
                    if user.role==1:
                        auth_login(request,user)
                        print(user.role)
                        return redirect('http://127.0.0.1:8000/')
                    elif user.role==2:
                        auth_login(request,user)
                        print(user.role)
                        return redirect('http://127.0.0.1:8000/publisherapp/pubindex/')
        else:
            error_message = "Please fill out all fields."
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')






def userlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')
        print(email)  # Print the email for debugging
        print(password)  # Print the password for debugging
        
        if email and password:
            user = authenticate(request, email=email, password=password)
            print("Authenticated user:", user)  # Print the user for debugging
            if user is not None and user.is_active:
                        
                        if user.is_active==False:
                                print("Inside user.is_active check")
                                auth_login(request, user)
                                print(user.is_active)
                                error_message = "Inactive login credentials."
                                return render(request, 'login.html', {'error_message': error_message})
                        else:

                            if user.role==1:
                                auth_login(request,user)
                                print(user.role)
                                return redirect('http://127.0.0.1:8000/')
                            elif user.role==2:
                                auth_login(request,user)
                                print(user.role)
                                return redirect('http://127.0.0.1:8000/accounts/sellerpage/')
                            elif user.role==3:
                                try:
                                    delivery_agent_profile = DeliveryAgentProfile.objects.get(user=user)
                                    auth_login(request, user)
                                    print(user.role)
                                    return redirect('http://127.0.0.1:8000/rest/deliveryagentdashboard/')
                                except DeliveryAgentProfile.DoesNotExist:
                                    auth_login(request, user)
                                    print(user.role)
                                    return redirect('http://127.0.0.1:8000/rest/deliveryagentprofile/')
                            else:
                                auth_login(request,user)
                                print(user.role)
                                return redirect('http://127.0.0.1:8000/accounts/admindashboard/')
        #         auth_login(request, user)
        #         print("User authenticated:", user.email, user.role)
        #         return redirect('http://127.0.0.1:8000/')
            
            # if user.is_active:
            #                     error_message = "Inactive login credentials."
            #                     return render(request, 'login.html', {'error_message': error_message})
            else:
                error_message = "Invalid Login Attempt"
                return render(request, 'login.html', {'error_message': error_message})
        # else:
        #     error_message = "Please fill out all fields."
        #     return render(request, 'login.html', {'error_message': error_message})

    return render(request,'login.html')












def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('sname')
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        role = User.CUSTOMER
        # print(first_name,last_name,password,role)
        if first_name and last_name and email  and role and password:
            if User.objects.filter(email=email).exists():
                error_message = "Email is already registered."
                return render(request, 'login.html', {'error_message': error_message})

            else:

                user = User(first_name=first_name, last_name=last_name, email=email, role=role)
                user.set_password(password)
                user.save()
                
                return redirect('login')

    return render(request, 'registration.html')


def seller(request):
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('sname')
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        role = User.SELLER
        print(first_name,last_name,password,role)
        if first_name and last_name and email and role and password:
            if User.objects.filter(email=email).exists():
                error_message = "Email is already registered."
                return render(request, 'login.html', {'error_message': error_message})

            else:

                user = User(first_name=first_name, last_name=last_name, email=email, role=role)
                user.set_password(password)
                user.save()
                return redirect('login')

    return render(request, 's_registration.html')



def logout(request):
    auth.logout(request)
    return redirect('index')


from django.shortcuts import get_object_or_404

def profile(request):
    user = request.user
    user_id = request.user.id
    books_in_count = BookCart.objects.filter(user_id=user_id).count()
    books_in_countw = Wishlist.objects.filter(user_id=user_id).count()

    # Try to get the UserProfile or create it if it doesn't exist
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        # Update user fields
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.phone_no = request.POST.get('phone_no')
        user.save()

        # Update user profile fields
        user_profile.country = request.POST.get('country')
        user_profile.state = request.POST.get('state')
        user_profile.city = request.POST.get('city')
        user_profile.district = request.POST.get('district')
        user_profile.phone_no = request.POST.get('phone_no')
        user_profile.addressline1 = request.POST.get('addressline1')
        user_profile.addressline2 = request.POST.get('addressline2')
        user_profile.pin_code = request.POST.get('pin_code')

        user_profile.save()

        return redirect('index')

    context = {
        'user': user,
        'user_profile': user_profile,
        'count':books_in_count,
        'countw':books_in_countw
    }
    return render(request, 'profile.html', context )


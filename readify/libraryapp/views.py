import datetime
from django.utils import timezone
from time import timezone
from django.shortcuts import render
from django.urls import reverse
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.contrib import messages
from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from .models import AddBook,BookCart, RentalRequest,Wishlist,AudioBook,PdfBook,LibraryAudio,LibraryPdf,On_payment,BookCategory, paymenthistory,Subscription, planSubscription
from django.db.models import Q
from django.http import JsonResponse
from xhtml2pdf import pisa
from django.views import View
from django.http import HttpResponse
from django.template.loader import get_template
from collections import defaultdict
from django.contrib.auth.decorators import login_required

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
# Create your views here.
@login_required(login_url='http://127.0.0.1:8000/login/')
def books_view(request):
    bookdata = AddBook.objects.all()
    categories = BookCategory.objects.all()
    user_id = request.user.id
    lockcart = BookCart.objects.filter(user_id=user_id)
    lockwish = Wishlist.objects.filter(user_id=user_id)
    wishlist_ids = [item.book.id for item in lockwish]
    print(wishlist_ids)
    # for book_id in lock_wishlist_ids:
    #     print(book_id)
    for book in lockwish:
        print(book.book_id)



    books_in_count = BookCart.objects.filter(user_id=user_id).count()
    books_in_countw = Wishlist.objects.filter(user_id=user_id).count()
    latest_subscription = planSubscription.objects.order_by('-startdate').first()
    # if  latest_subscription
    context ={
        'bookdata': bookdata ,
        'count':books_in_count,
        'countw':books_in_countw,
        'categories': categories,
        'latest_subscription':latest_subscription,
        'lockcart':lockcart,
        'lockwish':lockwish,
        'wishlist_ids':wishlist_ids,
    }
    return render(request,'books.html', context= context)

@login_required(login_url='http://127.0.0.1:8000/login/')
def books_view_category(request,category):
    b=BookCategory.objects.filter(name=category).first()
    bookdata = AddBook.objects.filter(category=b)
    categories = BookCategory.objects.all()
    return render(request,'books.html',{'bookdata': bookdata ,'categories': categories})
   
@login_required(login_url='http://127.0.0.1:8000/login/')
def live_search_books(request):
    query = request.GET.get('query')
    if query:
        books = AddBook.objects.filter(Q(id__icontains=query) | Q(title__icontains=query))
    else:
        books = AddBook.objects.all()
    
    book_list = []
    for book in books:
        # Create a dictionary for each book
        book_dict = {
            'id':book.id,
            'title': book.title,
            'author_name': book.author_name,
            'publisher': book.publisher,
            'summary': book.summary,
            'price': str(book.price),  # Convert Decimal to string
            'picture_url': book.picture.url,
        }
        book_list.append(book_dict)
    
    # Return the book data as JSON
    return JsonResponse({'bookdata': book_list})


 

from django.contrib import messages
@login_required(login_url='http://127.0.0.1:8000/login/')
def add_cart(request, bookid2):
    bookid = get_object_or_404(AddBook, id=bookid2)
    
    if bookid.stock <= 0:
        messages.warning(request, f"{bookid.title} is out of stock.")
    else:
        cart_item, created = BookCart.objects.get_or_create(user=request.user, book_id=bookid.id)
        cart_item.update_stock()
        cart_item.update_total()
        cart_item.save()
        if not created:
            cart_item.quantity += 1
            cart_item.update_total()
            # cart_item.cartstock -=1
            cart_item.save()

            # Update stock in AddBook model
            # bookid.stock -= 1
            # bookid.save()

            cart_item.update_stock()
            cart_item.save()

    return redirect('cart')

@login_required(login_url='http://127.0.0.1:8000/login/')
def decrease_item(request, item_id):
    try:
        cart_item = BookCart.objects.get(id=item_id)
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.cartstock +=1
            cart_item.update_total()
            cart_item.save()

            # Increase stock in AddBook model
            # cart_item.book.stock += 1
            # cart_item.book.save()
        else:
            messages.warning(request, f"{cart_item.book.title} is of stock empty.")
    except BookCart.DoesNotExist:
        pass  # Handle the case when the item does not exist in the cart

    return redirect('cart')

@login_required(login_url='http://127.0.0.1:8000/login/')
def increase_item(request, item_id):
    try:
        cart_item = BookCart.objects.get(id=item_id)
        
        if cart_item.cartstock > 1:
            cart_item.quantity += 1
            cart_item.cartstock -=1
            cart_item.update_total()
            cart_item.save()

            # Decrease stock in AddBook model
            # cart_item.book.stock -= 1
            # cart_item.book.save()
        else:
            messages.warning(request, f"{cart_item.book.title} is of stock empty.")
    except BookCart.DoesNotExist:
        pass  # Handle the case when the item does not exist in the cart

    return redirect('cart')


@login_required(login_url='http://127.0.0.1:8000/login/')
def cart(request):
    user_id = request.user.id  
    books_in_cart = BookCart.objects.filter(user_id=user_id)
    books_in_count = books_in_cart.count()
    books_in_countw = Wishlist.objects.filter(user_id=user_id).count()
    cartdata = BookCart.objects.all()
    book_details = AddBook.objects.filter(id__in=books_in_cart.values_list('book_id', flat=True))

    return render(request,"cart.html",{'cart_books':book_details , 'count':books_in_count,'countw':books_in_countw, 'cartdata': cartdata})

@login_required(login_url='http://127.0.0.1:8000/login/')
def delete_cart(request, cbye):
    remove=BookCart.objects.filter(book_id=cbye)
    remove.delete()
    return redirect('cart')

@login_required(login_url='http://127.0.0.1:8000/login/')
def add_wishlist(request, bookid3):
    bookid = get_object_or_404(AddBook, id=bookid3)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, book=bookid)
    
    if not created:
        wishlist_item.quantity += 1
        wishlist_item.save()

    return redirect('books_view')

@login_required(login_url='http://127.0.0.1:8000/login/')
def wishlist(request):
    user_id = request.user.id
    books_in_cart = Wishlist.objects.filter(user_id=user_id)
    books_in_count = BookCart.objects.filter(user_id=user_id).count()
    books_in_countw = Wishlist.objects.filter(user_id=user_id).count()
    book_details = AddBook.objects.filter(id__in=books_in_cart.values_list('book_id', flat=True))

    return render(request,"wishlist.html",{'books':book_details,'count':books_in_count,'countw':books_in_countw})

@login_required(login_url='http://127.0.0.1:8000/login/')
def delete_wishlist(request, bye):
    remove=Wishlist.objects.filter(book_id=bye)
    remove.delete()
    return redirect('wishlist')

@login_required(login_url='http://127.0.0.1:8000/login/')
def audio_view(request):
    return render(request,'audiobooks.html')

@login_required(login_url='http://127.0.0.1:8000/login/')
def audio_view(request):
    user_id = request.user.id
    audiobook = AudioBook.objects.all()
    books_in_count = BookCart.objects.filter(user_id=user_id).count()
    books_in_countw = Wishlist.objects.filter(user_id=user_id).count()
    context= {
        'count':books_in_count,
        'countw':books_in_countw,
        'audiobook':audiobook,
    }
    return render(request,'audiobooks.html',context)


@login_required(login_url='http://127.0.0.1:8000/login/')
def live_search_audio(request):
    query = request.GET.get('query')
    if query:
        books = AudioBook.objects.filter(Q(id__icontains=query) | Q(title__icontains=query))
    else:
        books = AudioBook.objects.all()
    
    book_list = []
    for book in books:
        # Create a dictionary for each book
        book_dict = {
            'id':book.pk,
            'title': book.title,
            'author': book.author,
            'duration': str(book.duration),
            'narrator': book.narrator,
            'publication_date': book.publication_date,
            'cover_image': book.cover_image.url,
            'audio_file' : book.audio_file.url,
            
        }
        book_list.append(book_dict)
        # print(book_list)
    
    # Return the book data as JSON
    return JsonResponse({'bookdata': book_list})

@login_required(login_url='http://127.0.0.1:8000/login/')
def pdf_view(request):
    pdfbook = PdfBook.objects.all()
    
    return render(request,'pdfbooks.html', {'pdfbook':pdfbook})

@login_required(login_url='http://127.0.0.1:8000/login/')
def live_search_pdf(request):
    query = request.GET.get('query')
    if query:
        books = PdfBook.objects.filter(Q(id__icontains=query) | Q(title__icontains=query))
    else:
        books = PdfBook.objects.all()
    
    book_list = []
    for book in books:
        # Create a dictionary for each book
        book_dict = {
            'id':book.id,
            'title': book.title,
            'author_name': book.author_name,
            'page_number': str(book.page_number),
            'cover_image': book.cover_image.url,
            'pdf_file' : book.pdf_file.url,
            
        }
        book_list.append(book_dict)
        # print(book_list)
    
    # Return the book data as JSON
    return JsonResponse({'bookdata': book_list})

@login_required(login_url='http://127.0.0.1:8000/login/')
def libary_view(request):
    user_id = request.user.id
    audio_in_libary =LibraryAudio.objects.filter(user_id=user_id)
    audio_details = AudioBook.objects.filter(id__in=audio_in_libary.values_list('audio_id', flat=True))
    pdf_in_libary = LibraryPdf.objects.filter(user_id=user_id)
    pdf_details = PdfBook.objects.filter(id__in=pdf_in_libary.values_list('pdf_id', flat=True))
    
    books_in_count = BookCart.objects.filter(user_id=user_id).count()
    books_in_countw = Wishlist.objects.filter(user_id=user_id).count()
    context = {
        'count':books_in_count,
        'countw':books_in_countw,
        'libaryaudio':audio_details , 
        'libarypdf' : pdf_details
    }
    return render(request,'library.html',context)

@login_required(login_url='http://127.0.0.1:8000/login/')
def add_audiotolibrary(request, audioid):
    userid=request.user.id
    audiobook = LibraryAudio(
        user_id=userid,
        audio_id=audioid        
    )
    audiobook.save()
    return redirect('audio_view')

@login_required(login_url='http://127.0.0.1:8000/login/')
def delete_audiolibrary(request, bye):
    remove=LibraryAudio.objects.filter(audio_id=bye)
    # messages.warning(request, f"{remove.audio.title} is of removed.")
    remove.delete()
    return redirect('libary_view')

@login_required(login_url='http://127.0.0.1:8000/login/')
def add_pdftolibrary(request, pdfid):
    userid=request.user.id
    pdfbook = LibraryPdf(
        user_id=userid,
        pdf_id=pdfid,        
    )
    pdfbook.save()
    return redirect('pdf_view')

@login_required(login_url='http://127.0.0.1:8000/login/')
def delete_pdflibrary(request, bye):
    remove=LibraryPdf.objects.filter(pdf_id=bye)
    # messages.warning(request, f"{remove.audio.title} is of removed.")
    remove.delete()
    return redirect('libary_view')




@csrf_exempt
def paymenthandler(request):
    # Only accept POST request.
    if request.method == "POST":
        # Get the required parameters from the post request.
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        # Verify the payment signature.
        result = razorpay_client.utility.verify_payment_signature(params_dict)
        if result is not None:
            payment = On_payment.objects.get(razorpay_order_id=razorpay_order_id)
            amount = int(payment.amount * 100)

            # Capture the payment.
            razorpay_client.payment.capture(payment_id, amount)

            payment.payment_id = payment_id

            payment.payment_status = payment.PaymentStatusChoices.SUCCESSFUL
            payment.save()

            cart_items = BookCart.objects.all()
            total_quantity = sum(item.quantity for item in cart_items)
            
            bookcart_instances = BookCart.objects.filter(user=request.user)
            
            
            for bookcart_instance in bookcart_instances:
                add_book_instance = bookcart_instance.book
                add_book_instance.stock -= bookcart_instance.quantity
                add_book_instance.save()
                bookcart_instance.copy_to_paymenthistory()
                
                add_book_instance = bookcart_instance.book
            # book_instance.quantity -= total_quantity
            bookcart_instances.delete()
           

            # Render success page on successful capture of payment.
            # return redirect('cart')
            return render(request, 'success.html')
        else:
            # If there is an error while capturing payment.
            return render(request, 'paymentfail.html')
    else:
        # If signature verification fails.
        return HttpResponseBadRequest()


    
def payment(request,amt):
    cart_item = BookCart.objects.filter(user= request.user)
    currency = 'INR'
    amount = amt*100 
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = '/libraryapp/paymenthandler/'

    order = On_payment.objects.create(
        user=request.user,
        amount=amt,
        
        razorpay_order_id=razorpay_order_id,
        payment_status=On_payment.PaymentStatusChoices.PENDING,
    )

    # Add the products to the order
    for i in cart_item:
        order.book=i.book

    # Save the order to generate an order ID
    order.save()
 
    # we need to pass these details to frontend.
    context = {
        'cart_item': cart_item,
        'amount': amount,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,  # Set to 'total_price'
        'currency': currency,
        'callback_url': callback_url,
    }
 
    return render(request, 'payment.html', context=context)



@login_required(login_url='http://127.0.0.1:8000/login/')
def order_history(request):
    user_id = request.user.id
    order_history = paymenthistory.objects.filter(user_id=user_id)
    
    books_in_count = BookCart.objects.filter(user_id=user_id).count()
    books_in_countw = Wishlist.objects.filter(user_id=user_id).count()

    context = {
        'order_history': order_history,
        'count':books_in_count,
        'countw':books_in_countw,
    }

    return render(request, 'order_history.html', context)
 

def print_as_pdf(request, stid2):

    data = paymenthistory.objects.filter(id=stid2)
    
    if data:
        date = data[0].purchase_date
        # Extract day, hour, and minute from the purchase_date
        day = date.day
        hour = date.hour
        minute = date.minute

    # Filter using the extracted values
    payment = paymenthistory.objects.filter(purchase_date__day=day, purchase_date__hour=hour, purchase_date__minute=minute)
    total_amount = sum(i.stock_total for i in payment)
    
    template_path = 'template\invoice.html'  # Update with the actual path to your HTML template.

    # Context data to pass to the template
    context = {'data': payment,
               'total_amount': total_amount,
               }

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="contract_{stid2}.pdf"'

    # Render the HTML template to PDF
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()
        rendered_html = render(request, 'invoice.html', context)

        # Create a PDF using pisa
        pisa_status = pisa.CreatePDF(
            rendered_html.content,
            dest=response,
            link_callback=None  # Optional: Handle external links
        )
    return response


from django.db.models import Count
from django.http import HttpResponseForbidden

def rent(request, rentid):
    rent_details = get_object_or_404(AddBook, id=rentid)
    
    if request.method == 'POST':
        # Check if the user has already rented 3 books
        user = request.user
        total_books_rented = RentalRequest.objects.filter(user=user, request_status=RentalRequest.PaymentStatusChoices.SUCCESSFUL).count()
        if total_books_rented >= 3:
            # return HttpResponseForbidden("You can only rent up to 3 books at a time.")
            return HttpResponseRedirect(reverse('rent', args=[rentid]) + '?alert=book_limit_exceeded&book_id=')

        duration = int(request.POST.get('duration', 0))  # Convert to integer
        total = calculate_total(duration)
        rental_request = RentalRequest(
            user=user,
            book=rent_details,
            duration=duration,
            total=total,
        )
        rental_request.save()
        # Increment the total_books_rented after saving the current rental request
        # user.total_books_rented = total_books_rented + 1
        # user.save()
        return redirect('rentpayment',idpass=rental_request.id)
        # Redirect or return a response as needed

    return render(request, "rent.html", {'rent': rent_details})

def calculate_total(duration):
    rate_per_day = 5  # Assuming the rate is $15 per day
    total = duration * rate_per_day
    return total


@csrf_exempt
def renthandler(request):
    # Only accept POST request.
    if request.method == "POST":
        # Get the required parameters from the post request.
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        # Verify the payment signature.
        result = razorpay_client.utility.verify_payment_signature(params_dict)
        if result is not None:
            payment = RentalRequest.objects.get(razorpay_order_id=razorpay_order_id)
            amount = int(payment.total * 100)  # Use the total attribute instead of amount

            # Capture the payment.
            razorpay_client.payment.capture(payment_id, amount)

            # Update the request_status to indicate successful payment.
            payment.request_status = RentalRequest.PaymentStatusChoices.SUCCESSFUL
            payment.save()

            user = request.user
            total_books_rented = RentalRequest.objects.filter(user=user, request_status=RentalRequest.PaymentStatusChoices.SUCCESSFUL).count()
            user.total_books_rented = total_books_rented + 1
            user.save()
            


            return render(request, 'success.html')
        else:
            # If there is an error while capturing payment.
            return render(request, 'paymentfail.html')
    else:
        # If signature verification fails.
        return HttpResponseBadRequest()




def Rentpayment(request, idpass):
    rent_item = RentalRequest.objects.get(user=request.user, id=idpass)
    if rent_item:
        amount = rent_item.total*100
        currency = 'INR'
    else:
        # Handle the case when no rental request with the given ID is found
        # For example, you can redirect the user or render an error page
        pass

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = '/libraryapp/renthandler/'
    # wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, book=bookid)
    
    # if not created:
    #     wishlist_item.quantity += 1
    #     wishlist_item.save()
    if rent_item:
        rent_item.request_status = RentalRequest.PaymentStatusChoices.PAYMENT_PROCESSING
        rent_item.razorpay_order_id = razorpay_order_id
        rent_item.save()
    # Add the products to the order
    

    # Save the order to generate an order ID
    
 
    # we need to pass these details to frontend.
    context = {
        ''
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,  # Set to 'total_price'
        'currency': currency,
        'callback_url': callback_url,
    }
    return render(request, 'payment.html', context=context)

def view_rent(request):
   user= request.user
   rent_data=RentalRequest.objects.filter(user=user)
   return render(request, 'rent_view.html',{'rent_data':rent_data})


def subscription(request):
    plans = Subscription.objects.all()
    subscription = Subscription.objects.values().first()
    if subscription:
        features_str = subscription['features']  # Get the 'features' field as a string
        features = features_str.split(',') if features_str else []
    else:
        features = []
    return render(request, 'subscription.html',{'plans':plans,'features': features})



@csrf_exempt
def subscriptionhandler(request):
    # Only accept POST request.
    if request.method == "POST":
        # Get the required parameters from the post request.
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        # Verify the payment signature.
        result = razorpay_client.utility.verify_payment_signature(params_dict)
        if result is not None:
            payment = planSubscription.objects.get(razorpay_order_id=razorpay_order_id)
            amount = int(payment.price * 100)  # Use the total attribute instead of amount
            # Capture the payment.
            razorpay_client.payment.capture(payment_id, amount)

            # Update the request_status to indicate successful payment.
            
            payment.payment_status = planSubscription.PaymentStatusChoices.SUCCESSFUL
            payment.status =  planSubscription.StatusChoices.ACTIVE
            payment.save()

            payment.datechanger()

            return render(request, 'success.html')
        else:
            # If there is an error while capturing payment.
            return render(request, 'paymentfail.html')
    else:
        # If signature verification fails.
        return HttpResponseBadRequest()

 
def subscriptionpayement(request , plan):
    plan_item = Subscription.objects.get (id=plan)
    currency = 'INR'
    amount = plan_item.price*100
     
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))
  
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = '/libraryapp/subhandler/'
   
    item = planSubscription.objects.create(
        user = request.user,
        price=amount / 100,
        subid = plan_item,
        payment_status = planSubscription.PaymentStatusChoices.PAYMENT_PROCESSING,
        razorpay_order_id = razorpay_order_id,
        )
    item.save()
    # Add the products to the order
    

    # Save the order to generate an order ID
    
 
    # we need to pass these details to frontend.
    context = {
        ''
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,  # Set to 'total_price'
        'currency': currency,
        'callback_url': callback_url,
    }
    return render(request, 'payment.html', context=context)



def wallet(request):
     total_price = request.GET.get('totalPrice')

     if total_price is not None:
        # Do something with the total_price
        print("Total price:", total_price)
        # For example, you can pass it to a template as context
        return render(request, 'payment.html', {'total_price': total_price})
     else:
        # Handle the case when the 'totalPrice' parameter is not provided
        return HttpResponse("Total price not provided.")
        return render(request, 'Wallet.html')


def addwallet(request):
    
    return render(request ,'wallet')
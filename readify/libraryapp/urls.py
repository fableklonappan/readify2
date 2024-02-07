
from django.urls import path,include    
from django.conf import settings 
from django.conf.urls.static import static
from libraryapp import views
urlpatterns = [
     path('books_view/', views.books_view, name='books_view'),
     path('books_view/<str:category>/', views.books_view_category, name='books_view'),
     path('libraryapp/search/', views.live_search_books, name='live_search_books'),
     path('add_cart/<int:bookid2>/', views.add_cart, name='add_cart'),
     path('decrease_item/<int:item_id>/', views.decrease_item, name='decrease_item'),
     path('increase_item/<int:item_id>/', views.increase_item, name='increase_item'),
     path('cart',views.cart,name="cart"),
     path('delete_cart/<int:cbye>/', views.delete_cart, name='delete_cart'),
     path('add_wishlist/<int:bookid3>/', views.add_wishlist, name='add_wishlist'),
     path('wishlist',views.wishlist,name="wishlist"),
     path('delete_wishlist/<int:bye>/', views.delete_wishlist, name='delete_wishlist'),
     path('audio_view/', views.audio_view, name='audio_view'),
     path('libraryapp/searchaudio/', views.live_search_audio, name='live_search_audio'),
     path('pdf_view/', views.pdf_view, name='pdf_view'),
     path('libraryapp/searchpdf/', views.live_search_pdf, name='live_search_pdf'),
     path('library_view/', views.libary_view, name='libary_view'),
     path('add_audiotolibrary/<int:audioid>/', views.add_audiotolibrary, name='add_audiotolibrary'),
     path('delete_audiolibrary/<int:bye>/', views.delete_audiolibrary, name='delete_audiolibrary'),
     path('add_pdftolibrary/<int:pdfid>/', views.add_pdftolibrary, name='add_pdftolibrary'),
     path('delete_pdflibrary/<int:bye>/', views.delete_pdflibrary, name='delete_pdflibrary'),
     path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
     path('payment/<int:amt>', views.payment, name='payment'),
     path('order_history/', views.order_history, name='order_history'),
     path('print_as_pdf/<int:stid2>/', views.print_as_pdf, name='print_as_pdf'),
     path('rent/<int:rentid>/', views.rent, name='rent'),
     path('Rentpayment/<int:idpass>/', views.Rentpayment, name='rentpayment'),
      path('renthandler/', views.renthandler, name='renthandler'),
]
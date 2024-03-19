from django.contrib import admin
from .models import AddBook,BookCart,Wishlist,AudioBook,BookCategory,PdfBook
from .models import LibraryAudio,On_payment,paymenthistory,LibraryPdf,RentalRequest,Subscription,planSubscription

admin.site.register(BookCategory)
admin.site.register(AddBook)
admin.site.register(BookCart)
admin.site.register(On_payment)
admin.site.register(paymenthistory)
admin.site.register(Wishlist)
admin.site.register(AudioBook)
admin.site.register(LibraryAudio)
admin.site.register(PdfBook)
admin.site.register(LibraryPdf)
admin.site.register(RentalRequest)
admin.site.register(Subscription)
admin.site.register(planSubscription)
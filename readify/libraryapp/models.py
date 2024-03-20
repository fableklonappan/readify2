from django.db import models
from django.forms import ValidationError
from userapp.models import CustomUser
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
# Create your models here.

class BookCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class AddBook(models.Model):
    picture = models.ImageField(upload_to='books')
    title = models.CharField(max_length=200)
    author_name = models.CharField(max_length=100)
    publisher = models.CharField(max_length=200)
    summary = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ManyToManyField(BookCategory)
    stock = models.PositiveIntegerField(default=1)
    

    def __str__(self):
        return self.title
    
class BookCart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(AddBook, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    cartstock = models.PositiveIntegerField(default=1)
    stock_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def update_total(self):
        self.stock_total = self.quantity * self.book.price

    def copy_to_paymenthistory(self):
        # Create a new paymenthistory instance
        payment_history = paymenthistory(
            user=self.user,
            book=self.book,
            quantity=self.quantity,
            cartstock=self.cartstock,
            stock_total=self.stock_total,
            purchase_date=timezone.now()
        )
        payment_history.save()
    
    def update_stock(self):
        self.cartstock = self.book.stock

    
    def __str__(self):
        # return self.book.title
        return f"cart details {self.user.email}: {self.book.title}"
    

class On_payment(models.Model):  
    class PaymentStatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESSFUL = 'successful', 'Successful'
        FAILED = 'failed', 'Failed'
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user', null=True)
    # book = models.ForeignKey(AddBook, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Example field for amount as Decimal
    order_date = models.DateTimeField(auto_now_add=True)
    razorpay_order_id = models.CharField(max_length=255, default=None)
    payment_status = models.CharField(
        max_length=20, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.PENDING)
    
    def __str__(self):
        return self.user.first_name 
    
class paymenthistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(AddBook, on_delete=models.CASCADE, null=True)
    book_payment = models.ForeignKey(On_payment, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    cartstock = models.PositiveIntegerField(default=1)
    stock_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    purchase_date = models.DateTimeField()

    def str(self):
        return f"Purchase history for {self.user.username} - {self.purchase_date}"
      
    
class Wishlist(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    book=models.ForeignKey(AddBook,on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.book.title
    
class AudioBook(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    narrator = models.CharField(max_length=100)
    publication_date = models.DateField()
    cover_image = models.ImageField(upload_to='audiobook_covers/')
    audio_file = models.FileField(upload_to='audiobooks/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(BookCategory)
    def __str__(self):
        return self.title
    
class LibraryAudio(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    audio=models.ForeignKey(AudioBook,on_delete=models.CASCADE,null=True)
    
    
    def __str__(self):
        return self.audio.title
    

    
    
class PdfBook(models.Model):
    title = models.CharField(max_length=255)
    author_name = models.CharField(max_length=255)
    page_number = models.PositiveIntegerField()
    cover_image = models.ImageField(upload_to='pdf_covers/', blank=True, null=True)
    pdf_file = models.FileField(upload_to='book_pdfs/', blank=True, null=True)
    category = models.ManyToManyField(BookCategory)
                                 
    def __str__(self):
        return self.title
    
class LibraryPdf(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    pdf=models.ForeignKey(PdfBook,on_delete=models.CASCADE,null=True)
    
    
    def __str__(self):
        return self.pdf.title
    

class RentalRequest(models.Model):
    class PaymentStatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PAYMENT_PROCESSING = 'payment processing' ,'PAYMENT PROCESSING'
        SUCCESSFUL = 'successful', 'Successful'
        FAILED = 'failed', 'Failed'

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(AddBook, on_delete=models.CASCADE, null=True)
    duration = models.PositiveIntegerField()
    total = models.PositiveIntegerField(null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    request_status = models.CharField(
        max_length=20, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.PENDING)

    def __str__(self):
        return f"rent history for {self.user.first_name} - {self.book.title}"

class Subscription(models.Model):
    class nameplanStatusChoices(models.TextChoices):
        GOLD = 'Gold','GOLD'
        Premium ='premium','PREMIUM'
    nameplan =  models.CharField(max_length=255 , choices=nameplanStatusChoices.choices )
    date = models.DateTimeField(auto_now_add=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    duration = models.PositiveIntegerField()  # Duration in months
    features = models.CharField(max_length=255 , default='',) 

    


    def __str__(self):
        return f"{self.nameplan}'s Subscription"
    

class planSubscription(models.Model):
    class PaymentStatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PAYMENT_PROCESSING = 'payment processing' ,'PAYMENT PROCESSING'
        SUCCESSFUL = 'successful', 'Successful'
        FAILED = 'failed', 'Failed'
    class StatusChoices(models.TextChoices):
        EXPIRED = 'expired' ,'EXPIRED'
        ACTIVE = 'active' , 'ACTIVE'
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    subid=models.ForeignKey(Subscription,on_delete=models.CASCADE,null=True)
    price =models.PositiveIntegerField(null=True, blank=True)
    startdate = models.DateTimeField(auto_now_add=True)
    enddate = models.DateTimeField(null=True)
    razorpay_order_id = models.CharField(max_length=255, null=True) 
    status = models.CharField(
        max_length=20, choices=StatusChoices.choices, default=StatusChoices.EXPIRED)
    payment_status = models.CharField(
        max_length=20, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.PENDING)
    
    def save(self, *args, **kwargs):
        current_date = timezone.now()
        if self.enddate and current_date.date() > self.enddate.date():
            self.status = "Expired"
        else:
            self.status = "Active"
        super().save(*args, **kwargs)

    def datechanger(self):
        if self.subid and self.subid.duration and self.startdate:
            self.enddate = self.startdate + timedelta(days=30 * self.subid.duration)
            self.save()

    def __str__(self):
        return f"Subscription plan for {self.user.first_name} - {self.subid.nameplan}"
    

class walletdata(models.Model):
    class PaymentStatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PAYMENT_PROCESSING = 'payment processing' ,'PAYMENT PROCESSING'
        SUCCESSFUL = 'successful', 'Successful'
        FAILED = 'failed', 'Failed'

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    total = models.PositiveIntegerField(null=True, blank=True, default=0)
    order_date = models.DateTimeField(auto_now_add=True)
    razorpay_order_id = models.CharField(max_length=255, null=True)
    request_status = models.CharField(
        max_length=20, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.PENDING)
    


    def __str__(self):
        return f"rent history for {self.user.first_name} - {self.request_status}"


class copywalletdata(models.Model):  # Capitalize Model
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    total = models.PositiveIntegerField(null=True, blank=True, default=0)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s --- {self.total}"
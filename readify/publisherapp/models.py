from django.db import models

from libraryapp.models import RentalRequest, paymenthistory, planSubscription
from userapp.models import CustomUser

# Create your models here.
class ViewCustomer(models.Model):
    name = models.CharField(max_length=100)
    order = models.CharField(max_length=100,null = True)  
    rent = models.CharField(max_length=100,null =True)   
    sub = models.CharField(max_length=100,null=True)    

    def __str__(self):
        return self.name
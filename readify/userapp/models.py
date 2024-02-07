from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, fname, sname, email, pwd=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=fname,
            last_name=sname,
            **extra_fields,
        )
        user.set_password(pwd)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(first_name, last_name, email, password, **extra_fields)

class CustomUser(AbstractUser):
    CUSTOMER = 1
    SELLER = 2

    ROLE_CHOICES = (
        (CUSTOMER, 'Customer'),
        (SELLER, 'Seller'),
    )
    username=None
    USERNAME_FIELD = 'email'
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    total_books_rented=  models.PositiveIntegerField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    
    
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    district = models.CharField(max_length=15, blank=True, null=True)
    addressline1 = models.CharField(max_length=15, blank=True, null=True)
    addressline2 = models.CharField(max_length=15, blank=True, null=True)
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.user:
            return self.user.first_name
        else:
            return "UserProfile with no associated user"
        
     
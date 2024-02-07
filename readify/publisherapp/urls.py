
from django.urls import path,include    
from django.conf import settings 
from django.conf.urls.static import static
from publisherapp import views
urlpatterns = [
    path('pubindex/', views.pubindex, name='pubindex'),


    ]
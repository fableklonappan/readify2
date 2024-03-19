
from django.urls import path,include    
from django.conf import settings 
from django.conf.urls.static import static
from publisherapp import views
urlpatterns = [
    path('logout/',views.logout,name='logout'),
    path('pubindex/', views.pubindex, name='pubindex'),
    path('s_rent/', views.s_rent, name='s_rent'),

    ]
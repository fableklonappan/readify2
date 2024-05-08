
from django.urls import path,include    
from django.conf import settings 
from django.conf.urls.static import static
from publisherapp import views
urlpatterns = [
    path('logout/',views.logout,name='logout'),
    path('pubindex/', views.pubindex, name='pubindex'),
    path('s_rent/', views.s_rent, name='s_rent'),
    path('view/', views.viewcust, name='viewcust'),
    path('viewid/<int:cusid>', views.detilescust, name='detilescust'),
    path('addbook/', views.addbook, name='addbook'),
    path('add_audiobook/', views.add_audiobook, name='add_audiobook'),
    ]
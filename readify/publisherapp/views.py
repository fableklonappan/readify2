from django.shortcuts import render

# Create your views here.
def pubindex(request):
    
    return render(request,'publisher.html')
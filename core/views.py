from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def ai(request):
    return render(request, 'ai.html')

def cybersecurity(request):
    return render(request, 'cybersecurity.html')

def gaming(request):
    return render(request, 'gaming.html')

def trending(request):
    return render(request, 'trending.html')
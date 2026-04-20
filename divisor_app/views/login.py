# divisor_app/views/login.py

from django.shortcuts import render

def login_view(request):
    return render(request, 'divisor_app/login.html')

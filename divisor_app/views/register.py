# divisor_app/views/register.py

from django.shortcuts import render

def register_view(request):
    return render(request, 'divisor_app/register.html')

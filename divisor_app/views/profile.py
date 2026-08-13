#! divisor_app/views/profile.py

from django.shortcuts import render


def profile_view(request):
    return render(request, "divisor_app/profile.html")

#! divisor_app/views/upgrade.py

from django.shortcuts import render


def upgrade_view(request):
    return render(request, "divisor_app/upgrade.html")

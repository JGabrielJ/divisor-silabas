from django.urls import path

from . import views

urlpatterns = [
    path("", views.main_view, name="main-view"),
    path("ads.txt", views.ads_txt, name="ads-txt"),
]

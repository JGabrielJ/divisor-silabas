# divisor_app/urls.py

from django.urls import path
from .views import (
    main,
    login,
    profile,
    upgrade,
    feedback,
    register,
)

urlpatterns = [
    path('', main.main_view, name='main-view'),
    path('login/', login.login_view, name='login-view'),
    path('profile/', profile.profile_view, name='profile-view'),
    path('upgrade/', upgrade.upgrade_view, name='upgrade-view'),
    path('feedback/', feedback.feedback_view, name='feedback-view'),
    path('register/', register.register_view, name='register-view'),
]

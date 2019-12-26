from django.urls import path, include

from account.views import *

urlpatterns = [
    path('login/', login_view, name='loginView'),
    path('password/', password_change_view, name='passwordChangeView'),
    path('register/', register_view, name='registerView'),
    path('logout/', logout_view, name='logoutView'),
]

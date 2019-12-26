from django.urls import path

from account.api.views import *

app_name = "apiAccount"

urlpatterns = [
    path('me/', ProfileView.as_view(), name='me'),
    path('change-password/', ChangePassword.as_view(), name='change-password'),
    path('register/', RegisterUser.as_view(), name='register'),
    #path('logout/', Logout.as_view(), name='logout'),
]
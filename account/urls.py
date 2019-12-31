from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from account import views

urlpatterns = [
    path('login/', views.login_view, name='loginView'),
    path('password/', views.password_change_view, name='passwordChangeView'),
    path('register/', views.register_view, name='registerView'),
    path('logout/', views.logout_view, name='logoutView'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

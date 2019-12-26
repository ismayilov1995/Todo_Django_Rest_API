from django.contrib import admin
from django.urls import path, include

from todos.views import mainPage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todos.urls')),
    path('auth/', include('account.urls')),
    path('api/', include('account.api.urls', namespace='apiAccount')),
    path('api/', include('todos.api.urls', namespace='apiTodos')),
]

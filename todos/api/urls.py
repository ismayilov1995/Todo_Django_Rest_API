from django.urls import path

from todos.api.views import *

app_name = "apiTodos"

urlpatterns = [
    path('list/', ListTodo.as_view(), name='list'),
    path('create/', CreateTodo.as_view(), name='createTodo'),
    path('detail/<id>/', TodoDetails.as_view(), name='detailTodo'),
    path('task/<id>/', TaskDetails.as_view(), name='detailTask'),
    path('add/<id>/', TaskDetailsNew.as_view(), name='addTask'),
]
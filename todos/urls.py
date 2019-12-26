from django.urls import path, include

from todos.views import *

urlpatterns = [
    path('', mainPage, name='mainPage'),
    path('add-todo/', add_todo, name='addTodo'),
    path('add-task/', add_task, name='addTask'),
    path('check-task/', check_task, name='checkTask'),
    path('remove-todo/', remove_todo, name='removeTodo'),
    path('remove-task/', remove_task, name='removeTask'),
]

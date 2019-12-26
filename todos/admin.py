from django.contrib import admin

from todos.models import Todos, Tasks

admin.site.register(Todos)
admin.site.register(Tasks)

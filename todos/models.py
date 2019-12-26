from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404


class Todos(models.Model):
    user = models.ForeignKey(User, null=False, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=70, blank=False, null=False)
    deadline = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = 'Todo'
        ordering = ['-id']

    def __str__(self):
        return '{}: {}'.format(self.user.username, self.title)


    @classmethod
    def add_first_todo(cls, user, title, is_completed=False):
        new_todo = cls.objects.create(user=user, title=title, is_completed=is_completed)
        Tasks.objects.create(user=user, todos=new_todo, title=title, is_complete=is_completed)
        return new_todo


    def get_child_tasks(self):
        return Tasks.objects.filter(todos_id=self.id)

class Tasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    todos = models.ForeignKey(Todos, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=120, blank=False, null=False)
    is_complete = models.BooleanField()

    class Meta:
        verbose_name = 'Sub task'
        ordering = ['id']

    def __str__(self):
        return  '{}: {} - {}'.format(self.todos.user.username, self.todos.title, self.title)

    @classmethod
    def add_task(cls, user, todo_id, title, is_complete=False):
        todo = get_object_or_404(Todos, id=todo_id)
        new_task = Tasks.objects.create(user=user, todos=todo, title=title, is_complete=is_complete)
        return new_task
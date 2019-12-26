from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveDestroyAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated

from account.api.permissions import IsOwner, CanAddIfOwner
from todos.api.pagination import TodoPagination
from todos.api.serializers import TodoListSerializer, TodoCreateSerializer, TaskAddSerializer, TaskListDetailSerializer
from todos.models import Tasks, Todos

# Yeni to do ve siyahilar
class CreateTodo(CreateAPIView, ListModelMixin):
    serializer_class = TodoCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)

    # Mixin istifade edirik deye
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        if self.request.data.get('is_completed') == 'true':
            is_completed = True
        else:
            is_completed = False
        Todos.add_first_todo(self.request.user, self.request.data.get('title'), is_completed)


class ListTodo(ListAPIView):
    serializer_class = TodoListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TodoPagination

    def get_queryset(self):
        queryset = Todos.objects.filter(user=self.request.user)
        return queryset

class TodoDetails(RetrieveAPIView, RetrieveDestroyAPIView, CreateModelMixin):
    serializer_class = TodoListSerializer
    permission_classes = [IsOwner]
    lookup_field = 'id'

    def get_queryset(self):
        self.id = self.kwargs.get(self.lookup_field)
        return Todos.objects.filter(id=self.id)

class TaskDetailsNew(RetrieveAPIView, RetrieveDestroyAPIView, CreateModelMixin):
    serializer_class = TaskAddSerializer
    permission_classes = [IsOwner]
    lookup_field = 'id'

    def get_queryset(self):
        id = self.kwargs.get(self.lookup_field)
        return Todos.objects.filter(id=id)

    def post(self, request, *args, **kwargs):
         return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        id = self.kwargs.get('id')
        Tasks.add_task(self.request.user, id, self.request.data['title'], False)


class TaskDetails(RetrieveAPIView, RetrieveDestroyAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TaskListDetailSerializer
    permission_classes = [IsOwner]
    lookup_field = 'id'
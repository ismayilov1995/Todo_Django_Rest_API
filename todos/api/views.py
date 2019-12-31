from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveDestroyAPIView, \
    RetrieveUpdateDestroyAPIView, UpdateAPIView, get_object_or_404
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated

from account.api.permissions import IsOwner, CanAddIfOwner
from todos.api.pagination import TodoPagination
from todos.api.serializers import TodoListSerializer, TodoCreateSerializer, TaskAddSerializer, TaskListDetailSerializer, \
    TaskDetailUpdateSerializer
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



class TaskAddApi(RetrieveAPIView, RetrieveDestroyAPIView, CreateModelMixin):
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


class TaskDetails(RetrieveDestroyAPIView, UpdateAPIView):
    #serializer_class = TaskListDetailSerializer
    permission_classes = [IsOwner]
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return TaskDetailUpdateSerializer
        else: return TaskListDetailSerializer


    def get_queryset(self):
        id = self.kwargs.get(self.lookup_field)
        return Tasks.objects.filter(id=id)

    # Son task silinende to do da silinir
    def perform_destroy(self, instance):
        id = self.kwargs.get(self.lookup_field)
        task = get_object_or_404(Tasks, id=id)
        todo = get_object_or_404(Todos, id=task.todos_id)
        instance.delete()
        if not Tasks.objects.filter(todos=todo).exists():
            todo.delete()

    # Update ederken 'PUT' useri deyishe bilmesin
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)




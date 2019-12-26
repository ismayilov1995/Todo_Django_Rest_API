from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from todos.models import Tasks, Todos

class TodoCreateSerializer(ModelSerializer):
    detail = serializers.HyperlinkedIdentityField(view_name='apiTodos:detailTodo', lookup_field='id')
    class Meta:
        model = Todos
        fields = ['title', 'deadline','is_completed','detail']

class TaskAddSerializer(ModelSerializer):
    class Meta:
        model = Todos
        exclude = ['is_completed']

    # Burda qalmisham
    #def create(self, validated_data):
        #Tasks.add_task(s)

# Bashqa modeli diger modelin icinde gostermeye calishiriq
class TaskListDetailSerializer(ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'


class TodoListSerializer(ModelSerializer):
    tasks = serializers.HyperlinkedIdentityField(view_name='apiTodos:detailTodo', lookup_field='id')
    # Bashqa modeli diger modelin icinde gostermeye calishiriq
    sub_task = SerializerMethodField()
    class Meta:
        model = Todos
        fields = '__all__'

    # Bashqa modeli diger modelin icinde gostermeye calishiriq
    def get_sub_task(self, obj):
        return TaskListDetailSerializer(obj.get_child_tasks(), many=True).data
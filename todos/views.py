from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from todos.models import Todos, Tasks

@login_required()
def mainPage(request):
    todo = Todos.objects.filter(user= request.user)
    return render(request, 'main_page.html', {'todo': todo})

@login_required()
def add_todo(request):
    if not request.is_ajax():
        return HttpResponseForbidden()
    user = request.user
    task = request.POST.get('content')
    todo = Todos.add_first_todo(user=user, title=task)
    html = render_to_string('include/todo/single-todo-card.html', {'td': todo})
    data = {'is_valid': True, 'task': task, 'html': html}
    return JsonResponse(data=data)

@login_required()
def remove_todo(request):
    if not request.is_ajax():
        return HttpResponseForbidden()
    todo = get_object_or_404(Todos, pk=request.GET.get('pk'))
    todo.delete()
    return JsonResponse(data={"is_valid":True})

@login_required()
def remove_task(request):
    if not request.is_ajax():
        return HttpResponseForbidden()
    todo = get_object_or_404(Todos, id=request.GET.get('todo_id'))
    task = get_object_or_404(Tasks, pk=request.GET.get('pk'))
    data = {'is_valid': True, 'has_todo': True}
    task.delete()
    if not Tasks.objects.filter(todos=todo).exists():
        todo.delete()
        data['has_todo'] = False
    return JsonResponse(data=data)

@login_required()
def add_task(request):
    if not request.is_ajax():
        return HttpResponseForbidden()
    if request.method == 'GET':
        li_html = render_to_string('include/each-task-li-add.html')
        return JsonResponse(data={"is_valid": True, 'html': li_html})
    else:
        todo_id = request.POST.get('todo_id')
        task = request.POST.get('content')
        new_task = Tasks.add_task(request.user, todo_id, task)
        li_html = render_to_string('include/each-task-li.html', {'tk': new_task})
        return JsonResponse(data={"is_valid": True, 'html': li_html})

@login_required()
def check_task(request):
    if not request.is_ajax():
        return HttpResponseForbidden()
    task = get_object_or_404(Tasks, id=request.GET.get('checked_task'))
    if task.is_complete:
        task.is_complete = False
        is_checked = False
    else:
        task.is_complete = True
        is_checked = True
    task.save()
    return JsonResponse({"is_checked": is_checked})
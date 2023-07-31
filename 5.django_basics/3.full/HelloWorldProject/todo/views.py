from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo

def todo_list(request):
    todos = Todo.objects.all()
    return render(request, 'todo/todo_list.html', {'todos': todos})

def todo_detail(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    return render(request, 'todo/todo_detail.html', {'todo': todo})

def todo_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        todo = Todo.objects.create(title=title, description=description)
        return redirect('todo_detail', pk=todo.pk)
    return render(request, 'todo/todo_create.html')

def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        todo.title = title
        todo.description = description
        todo.save()
        return redirect('todo_detail', pk=todo.pk)
    return render(request, 'todo/todo_update.html', {'todo': todo})

def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    return redirect('todo_list')

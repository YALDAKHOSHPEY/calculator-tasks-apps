from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

class TaskForm(forms.Form):
    """Form for creating and editing tasks"""
    task = forms.CharField(
        label="Task Description",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your task here',
            'class': 'task-input'
        })
    )

def index(request):
    """Display the list of tasks"""
    if "tasks" not in request.session:
        request.session["tasks"] = []
    
    return render(request, "tasks/index.html", {
        "tasks": enumerate(request.session["tasks"], start=1)  # Start counting from 1 for better UX
    })

def add(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"].append(task)
            request.session.modified = True
            return redirect("tasks:index")
    
    return render(request, "tasks/add.html", {
        "form": TaskForm()
    })

def edit(request, task_index):
    """Handle task editing"""
    try:
        task_list = request.session["tasks"]
        task_content = task_list[task_index]
        
        if request.method == "POST":
            form = TaskForm(request.POST)
            if form.is_valid():
                edited_task = form.cleaned_data["task"]
                task_list[task_index] = edited_task
                request.session.modified = True
                return redirect("tasks:index")
        
        initial_data = {'task': task_content}
        return render(request, "tasks/edit.html", {
            "form": TaskForm(initial=initial_data),
            "task_index": task_index
        })
    
    except (IndexError, KeyError):
        return redirect("tasks:index")  # Handle invalid task_index gracefully

def delete(request, task_index):
    """Handle task deletion"""
    if request.method == "POST":
        try:
            del request.session["tasks"][task_index]
            request.session.modified = True
        except (IndexError, KeyError):
            pass  # Silently handle errors for invalid indexes
        
        return redirect("tasks:index")
    
    try:
        task_content = request.session["tasks"][task_index]
        return render(request, "tasks/delete.html", {
            "task": task_content,
            "task_index": task_index
        })
    except (IndexError, KeyError):
        return redirect("tasks:index")
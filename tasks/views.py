from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")

def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request, "tasks/index.html", {
        "tasks": enumerate(request.session["tasks"])  # Add enumerate here
    })

def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task]
            request.session.modified = True
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/add.html", {
                "form": form
            })
    return render(request, "tasks/add.html", {
        "form": NewTaskForm()
    })

def edit(request, task_index):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            edited_task = form.cleaned_data["task"]
            request.session["tasks"][task_index] = edited_task
            request.session.modified = True
            return HttpResponseRedirect(reverse("tasks:index"))
    
    initial_data = {'task': request.session["tasks"][task_index]}
    return render(request, "tasks/edit.html", {
        "form": NewTaskForm(initial=initial_data),
        "task_index": task_index  # Make sure to pass task_index to template
    })

def delete(request, task_index):
    if request.method == "POST":
        del request.session["tasks"][task_index]
        request.session.modified = True
        return HttpResponseRedirect(reverse("tasks:index"))
    
    return render(request, "tasks/delete.html", {
        "task": request.session["tasks"][task_index],
        "task_index": task_index
    })
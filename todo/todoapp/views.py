from django.http import HttpResponseRedirect
from urllib.parse import urlparse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, login as customlogin
from django.contrib import messages

from .forms import taskForm
from .models import task
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'todoapp/index.html',{})


def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        # firstname = request.POST.get('firstname')
        # lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 3:
            messages.error(request, 'Password must be at least 3 characters')
            return HttpResponseRedirect('/register')

        get_all_users_by_username = User.objects.filter(username=username)
        if get_all_users_by_username:
            messages.error(request, 'Error, username already exists, Use another.')
            return HttpResponseRedirect('/register')

        new_user = User.objects.create_user( username=username, email=email, password=password)
        new_user.is_active = True
        # new_user.firstname = firstname
        # new_user.lastname = lastname
        new_user.save()
        messages.success(request, 'User successfully created, login now')
        return redirect('/login')
    return render(request, 'todoapp/register.html', {})


def login(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            customlogin(request, validate_user)
            return redirect('/')
        else:
            messages.error(request, 'Error, wrong user details or user does not exist')
            return redirect('login')
    return render(request, 'todoapp/login.html' )


def logoutview(request):
    logout(request)
    return redirect('login')



def createtask(request):
    if request.method == 'POST':
        taskname = request.POST.get('taskname')
        dadeline = request.POST.get('dadeline')
        status = request.POST.get('status')
        details = request.POST.get('details')
        comment = request.POST.get('comment')
        new_task = task(user=request.user, taskname=taskname, dadeline=dadeline, status=status, details=details, comment=comment)
        new_task.save()
        return HttpResponseRedirect('/task-list')

    all_task = task.objects.filter(user=request.user)
    context = {
        'task': all_task
    }
    return render(request, 'todoapp/create-task.html', context)


def tasklist(request):
    all_task = task.objects.filter(user=request.user)
    context = {
        'task': all_task
    }
    return render(request, 'todoapp/task-list.html', context)



@login_required
def deletetask(request, name):
    get_task = task.objects.get(user=request.user, taskname=name)
    get_task.delete()
    return redirect('/task-list')



def edit(request, id):
    task_model = task.objects.get(id=id)
    dadeline = task_model.dadeline.strftime("%Y-%m-%d %H:%M:%S")
    if request.method == 'POST':
        task_model.taskname = request.POST.get('taskname')
        task_model.dadeline = request.POST.get('dadeline')
        task_model.status = request.POST.get('status')
        task_model.details = request.POST.get('details')
        task_model.comment = request.POST.get('comment')
        task_model.save()
        return redirect('/task-list')
    return render(request, 'todoapp/update-task.html', {'task': task_model, "dadeline": dadeline})



def detailsview(request, id):
    get_task = task.objects.get(id=id)
    return render(request, 'todoapp/details.html', {'task': get_task})

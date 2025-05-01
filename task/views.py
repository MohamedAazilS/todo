from django.shortcuts import render, redirect
from .models import ToDo, ToDoUser
from .forms import ToDoForm, RegisterForm, LoginForm
from django.http import HttpResponseRedirect
from rest_framework import viewsets
from .serilizers import ToDOSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny , IsAuthenticated, IsAdminUser
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def task_list(req):
    tasks = ToDo.objects.all()
    if req.method == "POST":
        status = req.POST.get('status', False)
        if status != "none":
            # tasks = tasks.objects.filter(status = status)
            user = ToDoUser.objects.get(username = req.user.username)
            tasks = tasks.filter(user = user, status = status)
    else:
        user = ToDoUser.objects.get(username = req.user.username)
        tasks = ToDo.objects.filter(user = user)
        
    user = ToDoUser.objects.get(username = req.user.username)
    tasks = tasks.filter(user = user)
    return render(req, "task_list.html", {"tasks":tasks})
@login_required
def task_desc(req, id):
    task = ToDo.objects.get(id = id)
    return render(req, 'task_desc.html', {"task" : task})
@login_required
def task_delete(req, id):
    task = ToDo.objects.get(id = id)
    task.delete()
    tasks = ToDo.objects.all()
    return render(req,"task_list.html", {"tasks":tasks})
@login_required
def task_create(req):
    form = ToDoForm()
    if req.method == "POST":
        form = ToDoForm(req.POST)
        if form.is_valid():
            task = ToDo.objects.create(
                name = form.cleaned_data['name'],
                desc = form.cleaned_data['desc'],
                priority = form.cleaned_data['priority'],
                status = form.cleaned_data['status'],
                user = ToDoUser.objects.get(username = req.user.username)
            )
            task.save()
            return HttpResponseRedirect(f"{task.id}")
        
    return render(req, "task_create.html", {"form" : form}) 

@login_required
def task_update(req, id):
    task = ToDo.objects.get(id = id)
    form = ToDoForm(instance=task)
    if req.method == "POST":
        form = ToDoForm(req.POST,instance=task)
        if form.is_valid():
            task.save()
            return render(req, "task_desc.html", {"task":task})
        else:
            form = ToDoForm(instance=task)
    return render(req, "task_create.html", {"form":form})


class TaskViewSet(viewsets.ModelViewSet):
    queryset = ToDo.objects.all()
    serializer_class = ToDOSerializer
    
    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.request.method != "GET":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
def register(req):
    form = RegisterForm()
    if req.method == "POST":
        form = RegisterForm(req.POST)
        if form.is_valid():
            form.save()
            reg_user = ToDoUser.objects.create(
                username = form.cleaned_data['username']
            )
            reg_user.save()
            user = authenticate(req,username = form.cleaned_data['username'],password = form.cleaned_data['password1'])
            auth.login(req, user)
            return redirect("/task")
    context = {"form":form}
    return render(req, "register.html", context)

def user_login(req):
    form = LoginForm()
    if req.method == "POST":
        form = LoginForm(req, data = req.POST)
        if form.is_valid():
            username = req.POST.get("username")
            password = req.POST.get("password")

            user = authenticate(req,username = username,password = password)
            
            if user is not None:
                auth.login(req, user)
                return redirect("/task")

    return render(req, "login.html", {"form":form})

def user_logout(req):
    auth.logout(req)
    return redirect("/task/login")
from datetime import datetime
import random
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    return render(request, "index.html")


def profile(request):
    if request.user.is_authenticated:
        passwords = []
        #if delte
        for a in Passwords.objects.all().filter(user=request.user):
            if a.date_del:
                if a.date_del <= datetime.now().date():
                    a.delete()

            b = int(a.password[0])
            a.password = a.password[1:len(a.password)]
            c = ""
            for i in a.password:
                c += chr(ord(i)-b)
            a.password = c
            passwords.append(a)
        items = reversed(passwords)
        items2 = reversed(passwords)
        return render(request, "profile.html", {'items':items, 'items2':items2})
    else:
        return render(request, "sign.html")


def sign_up(request):
    username = str(request.POST['name'])
    for n in User.objects.all():
        if username == n.username:
            return JsonResponse({"status": "name"})
    User.objects.create_user(username=username, email=str(request.POST['email']),
                             password=str(request.POST['password']))
    return JsonResponse({"status": "ok"})


def sign_in(request):
    username = request.POST['name']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"status": "ok"})

    return JsonResponse({"status": "error"})


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('index')
    else:
        return redirect('index')

def new_item(request):
    if not request.user.is_authenticated:
        return redirect('profile')
    return render(request, "new_item.html")

def add_new_item(request):
    if request.user.is_authenticated:
        web = request.POST['web']
        for p in Passwords.objects.all().filter(user=request.user):
            if web == p.domain:
                return JsonResponse({"status":"web"})
        username = request.POST['username']
        password = request.POST['password']
        del_date = request.POST['del_date']

        random_number = random.randint(0,9)
        new_password = f"{random_number}"
        for i in password:
            a = ord(i)+random_number
            a = chr(a)
            new_password +=a

        if del_date:
            Passwords(user=request.user, domain=web, username=username, password=new_password, date_del=del_date).save()
        elif not del_date:
            Passwords(user=request.user, domain=web, username=username, password=new_password).save()

        return JsonResponse({"status":"ok"})
    return redirect('profile')

def change(request):
    if request.user.is_authenticated:
        id = int(request.POST['id'])
        web = request.POST['web']
        this = Passwords.objects.all().get(id=id)
        for p in Passwords.objects.all().filter(user=request.user):
            if web == p.domain and this.domain != web:
                return JsonResponse({"status": "web"})
        username = request.POST['username']
        password = request.POST['password']
        del_date = request.POST['del_date']

        random_number = random.randint(0,9)
        new_password = f"{random_number}"
        for i in password:
            a = ord(i)+random_number
            a = chr(a)
            new_password +=a

        this.domain = web
        this.username = username
        this.password = new_password
        if del_date:
            this.date_del = del_date
        this.save()

        return JsonResponse({"status": "ok"})
    return redirect('profile')

def delete_item(request):
    domain = request.POST['domain']
    Passwords.objects.all().get(domain=domain).delete()
    return JsonResponse({"status":"ok"})

def chage_user(request):
    if request.user.is_authenticated:
        user = request.user
        name = request.POST['name']
        for n in User.objects.all():
            if name == n.username:
                return JsonResponse({"status": "name"})
        email = request.POST['email']
        password = request.POST['password']
        user.username = name
        user.email = email
        user.set_password(password)
        user.save()
        return JsonResponse({"status":"ok"})
    return JsonResponse({"status":"ok"})
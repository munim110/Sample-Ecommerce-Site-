import email
from django.shortcuts import redirect, render
from django.db import connection
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from Product.models import *


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            string = request.POST.get('search')
            return redirect(search_view, string=string)
        else:
            all_products = Product.objects.all()
            return render(request, 'Home/home.html', {'all_products': all_products})
    else:
        return redirect(signin)

def search_view(request,string):
    if string is not None and string != '':
        all_products = Product.objects.filter(name__contains=string)
    else:
        all_products = Product.objects.all()
    return render(request, 'Home/search_result.html', {'all_products': all_products})

def signin(request):
    logout(request.user) if request.user.is_authenticated else None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(home)
        else:
            return HttpResponse("Login Failed! Wrong username or password")
    return render(request, 'Userauth/login.html')

def userprofile(request):
    if request.user.is_authenticated:
        return render(request, 'Userauth/userprofile.html',{'name':request.user.get_full_name(),
        'email':request.user.email,
        'username':request.user.username})
    else:
        return redirect(signin)

def editinfo(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email')
            user = request.user
            if firstname is not None or firstname != "":
                user.first_name = firstname
            if lastname is not None or lastname != "":
                user.last_name = lastname
            if email is not None or email != "":
                if User.objects.filter(email=email).exists():
                    return HttpResponse("Email already exists")
                else:
                    user.email = email
            user.save()
            return HttpResponse("User updated successfully")
        else:
            return render(request, 'Userauth/edituser.html',{'firstname':request.user.first_name,
            'lastname':request.user.last_name,'email':request.user.email, })

    else:
        return redirect(home)

def changepassword(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user
            oldpassword = request.POST.get('oldpassword')
            newpassword = request.POST.get('newpassword')
            newpassword2 = request.POST.get('newpassword2')
            if user.check_password(oldpassword):
                if newpassword == newpassword2:
                    user.set_password(newpassword)
                    user.save()
                    return HttpResponse("Password changed successfully")
                else:
                    return HttpResponse("Passwords do not match")
            else:
                return HttpResponse("Old password is incorrect")
        else:
            return render(request, 'Userauth/changepass.html')
    else:
        return redirect(home)

def signup(request):
    if request.user.is_authenticated:
        return redirect(home)
    if request.method == "POST":
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password == password2:
            if User.objects.filter(username=username).exists():
                return HttpResponse("Username already exists")
            elif User.objects.filter(email=email).exists():
                return HttpResponse("Email already exists")
            else:
                try:
                    user = User.objects.create_user(username=username, password=password, email=email, first_name=firstname, last_name=lastname)
                    user.save()
                    return HttpResponse("User created successfully")
                except:
                    return HttpResponse("Error")
        else:
            return HttpResponse("Passwords do not match")
            

    else: 
        return render(request, 'Userauth/signup.html')



def signout(request):
    logout(request)
    return redirect(home)
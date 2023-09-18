import random
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime
from django.shortcuts import render
from capitalsscopeproj.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserOTP
from .forms import CreateUserForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.shortcuts import (HttpResponse, HttpResponseRedirect, redirect,render)
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,UserCreationForm)

# Create your views here.

def home(request):
    return render(request, 'views_reg/home.html')

def home1(request):
    return render(request, 'views_reg/home1.html')


def home2(request):
    return render(request, 'views_reg/home2.html')

def About(request):
    return render(request, 'views_reg/about.html')

def About1(request):
    return render(request, 'views_reg/about1.html')

def Services(request):
    return render(request, 'views_reg/services.html')

def Services1(request):
    return render(request, 'views_reg/services1.html')

def Portfolio(request):
    return render(request, 'views_reg/portfolio.html')

def PortfolioDeatils(request):
    return render(request, 'views_reg/portfolio-details.html')

def Portfolio1(request):
    return render(request, 'views_reg/portfolio1.html')

def PortfolioDeatils1(request):
    return render(request, 'views_reg/portfolio-details1.html')

def Team(request):
    return render(request, 'views_reg/team.html')

def Team1(request):
    return render(request, 'views_reg/team1.html')

def Blog(request):
    return render(request, 'views_reg/blog.html')

def BlogDetails(request):
    return render(request, 'views_reg/blog-details.html')

def Blog1(request):
    return render(request, 'views_reg/blog1.html')

def BlogDetails1(request):
    return render(request, 'views_reg/blog-details1.html')

def PagesLogin(request):
    return render(request, 'views_reg/pages-login.html')

def PagesRegister(request):
    return render(request, 'views_reg/pages-register.html')

def Contactus(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact = Contact(name=name, email=email, subject=subject, message=message, date=datetime.today())
        contact.save()
    return render(request, 'views_reg/contact-new.html')

def Contactus1(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact = Contact(name=name, email=email, subject=subject, message=message, date=datetime.today())
        contact.save()
    return render(request, 'views_reg/contact-new1.html')

def profile(request):
    if request.user.is_authenticated:
        
        return render(request, 'views_reg/users-profile.html',{'name':request.user})
    else:
        render(request, 'views_reg/users-profile.html')

def exxit(request):
    
    if request.user.is_authenticated:
        messages.success(request,'Logged out successfully !!')
        return render(request, 'views_reg/exit.html',{'name':request.user})
    else:
        return render(request, '/')

def Register_new(request):
    
    if request.method == 'POST':
        get_otp = request.POST.get('otp') #213243
        if get_otp:
            get_usr = request.POST.get('usr')
            usr = User.objects.get(username=get_usr)            
            if int(get_otp) == UserOTP.objects.filter(user = usr).last().otp:
                usr.is_active = True
                usr.save()
                messages.success(request,f'Account was created for {usr.username}')
                return redirect ('login_view')
            else:
                messages.warning(request,f'You Entered a Wrong OTP')
                return render (request, 'views_reg/pages-register1.html',{'otp':True, 'usr':usr})

        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            name = form.cleaned_data.get('name')#.split(' ')
            usr = User.objects.get(username=username)   
            usr.email = username
            usr.first_name = name#[0]
            usr.last_name = name[1]        
            usr.is_active = False
            print(username)
            print(name)
            usr.save()
            usr_otp = random.randint(100000,999999)
            UserOTP.objects.create(user=usr, otp=usr_otp)
            mess = f"Hello {usr},\nYour OTP is :- {usr_otp}\nThanks!"
            send_mail(
                "Welcome to Stock Analysis - Verify Your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently= False
                )
            return render (request, 'views_reg/pages-register1.html',{'otp':True, 'usr':usr})
            
    else:
        form = CreateUserForm()

    return render (request, 'views_reg/pages-register1.html',{'form':form})

def resend_otp(request):
    if request.method == "GET":
        get_usr = request.GET['usr']
        if User.objects.filter(username = get_usr).exists() and not User.objects.get(username = get_usr).is_active:
            usr = User.objects.get(username=get_usr)
            usr_otp = random.randint(100000,999999)
            UserOTP.objects.create(user=usr, otp=usr_otp)
            mess = f"Hello {usr},\nYour OTP is :- {usr_otp}\nThanks!"
            send_mail(
                "Welcome to Stock Analysis - Verify Your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently= False
                )
            return HttpResponse("Resend")
    
    return HttpResponse("Can't Send OTP")

def login_view(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    if request.method == 'POST':
        get_otp = request.POST.get('otp') #213243
        if get_otp:
            get_usr = request.POST.get('usr')
            usr = User.objects.get(username=get_usr)            
            if int(get_otp) == UserOTP.objects.filter(user = usr).last().otp:
                usr.is_active = True
                usr.save()
                login(request, usr)
                return redirect ('home1')
            else:
                messages.warning(request,f'You Entered a Wrong OTP')
                return render (request, 'views_reg/pages-login1.html',{'otp':True, 'usr':usr})

        form = LoginForm(request.POST)
        
        usrname = request.POST.get('username')
        passwd = request.POST.get('password')
        user = authenticate(request, username=usrname, password=passwd)
        if usrname == "mukeshkumarbairwa5686@gmail.com" and passwd == "vaa2829m":
            return redirect ('home2')
        elif user is not None:   
            
            login(request, user)
            
            return redirect ('home1')
        elif not User.objects.filter(username = usrname).exists():
            # request.sessions['is_logged'] = True     
            messages.success(request,f'Please enter a correct username and password')
            return redirect ('login_view')
        elif not User.objects.get(username = usrname).is_active:
            usr = User.objects.get(username = usrname)
            usr_otp = random.randint(100000,999999)
            UserOTP.objects.create(user=usr, otp=usr_otp)
            mess = f"Hello {usr},\nYour OTP is :- {usr_otp}\nThanks!"
            send_mail(
                "Welcome to Stock Analysis - Verify Your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently= False
                )

            return render (request, 'views_reg/pages-login1.html',{'otp':True, 'usr':usr})
        else:
            messages.success(request,f'Please enter a correct username and password')
            return redirect ('login_view')
    form = AuthenticationForm()    
    return render(request, 'views_reg/pages-login1.html', {'form':form})

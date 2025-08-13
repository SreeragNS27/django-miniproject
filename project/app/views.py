from django.shortcuts import render,redirect

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth import login,authenticate
from django.contrib.auth import logout
from django.contrib import messages
import random

from .models import client

# Create your views here.
def index(request):
    return render(request,'index.html')

def  about(request):
    return render(request,'about.html')
def services(request):
    return render(request,'services.html')
def blog(request):
    return render(request,'blog.html')
def blog_details(request):
    return render(request,'blog_details.html')
def contact(request):
    return render(request,'contact.html')

def elements(request):
    return render(request,'elements.html')


def register(request):
    if request.method == 'POST':
        name=request.POST['name']
        username=request.POST['username']
        age=request.POST['age']
        place=request.POST['place']
        email=request.POST['email']
        # if User.objects.filter(email=email).exists():
        #     return render(request,'register.html',{'error':'email already exists'})

        password=request.POST['password']
        data=User.objects.create_user(username=username,email=email,password=password)
        data.save()
        data1=client.objects.create(user_id=data,name=name,age=age,place=place)
        data1.save()
        send_mail(
                'Welcome to Appointment System',
                f'Hello {username}, your registration was successful!,your password is {password}',
                'nssreerag27@gmail.com',  
                [email],
                fail_silently=False,
            )
        return redirect(Login)
    
    else:
        return render(request,'register.html')


def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect(loginindex)

        else:
            return render(request,'login.html',{'error':"credentials are wrong "})
    else:
        return render(request,'login.html')
@login_required
def loginindex(request):
    return render(request,'loginindex.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def  loginabout(request):
    return render(request,'loginabout.html')
@login_required
def loginservices(request):
    return render(request,'loginservices.html')

@login_required
def logincontact(request):
    return render(request,'logincontact.html')

@login_required
def profile(request):

    data=User.objects.get(id=request.user.id)
    data1=client.objects.get(user_id=data)
    return render(request,'loginprofile.html',{'data':data1})

@login_required
def edit(request):
    data=User.objects.get(id=request.user.id)
    data1=client.objects.get(user_id=data)
    if request.method=='POST':
        data1.name=request.POST['name']
        data1.age=request.POST['age']
        data1.place=request.POST['place']
        data1.user_id.email=request.POST['email']
        data1.user_id.username=request.POST['username']
        data1.user_id.save()
        data1.save()
        return redirect(profile)
    else:
        return render(request,'profileedit.html',{"data":data1})
def send_otp(email):
    otp = random.randint(100000,999999)
    send_mail(
        'Your OTP Code',''
        f'Your OTP code is: {otp}',
        'nssreerag27@gmail.com',
        [email],
        fail_silently=False,
    )
    return otp

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            otp = send_otp(email)

            context = {
                        "email": email,
                        "otp": otp,
            }
            return render(request,'verify_otp.html',context)
        
        except User.DoesNotExist:
            messages.error(request,'Email address not found.')
    else:
        return render(request,'password_reset.html')
    return render(request,'password_reset.html') 

def verify_otp(request):
    if request.method == 'POST':
        email =request.POST.get('email')
        otpold = request.POST.get('otpold')
        otp = request.POST.get('otp')

        if otpold==otp :
            context = {
                'otp' : otp,
                'email': email
            }
            return render(request,'set_new_password.html',context)
        else:
            messages.error(request,"Invalid OTP")
    return render(request,'verify_otp.html') 

def set_new_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password==confirm_password:
            try:
               
                user=User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password has been reset successfully')
                return redirect(Login)
            except User.DoesNotExist:
                messages.error(request,'Password doesnot match')
        return render(request,'set_new_password.html',{'email':email})               
    return render(request,'set_new_password.html',{'email':email})




        




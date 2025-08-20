from django.shortcuts import render,redirect

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth import login,authenticate
from django.contrib.auth import logout
from django.contrib import messages
import random
from .models import client,Appointment
from datetime import datetime, date, time




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






# Define available slots (you can customize)
AVAILABLE_SLOTS = [
    time(9, 0),
    time(10, 0),
    time(11, 0),
    time(14, 0),
    time(15, 0),
    time(16, 0),
]

@login_required
def book_appointment(request):
    # 1️⃣ Get selected date (from GET or default today)
    selected_date_str = request.GET.get('date')
    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        except ValueError:
            selected_date = date.today()
    else:
        selected_date = date.today()

    # 2️⃣ Find already booked slots for that date
    booked_slots = list(
        Appointment.objects.filter(date=selected_date).values_list('time', flat=True)
    )
    slots = [
        {"time": s, "booked": s in booked_slots} for s in AVAILABLE_SLOTS
    ]

    # 3️⃣ Handle booking submission
    if request.method == "POST":
        name = request.POST['name']
        age = request.POST['age']
        email = request.POST['email']
        phone = request.POST['phone']

        # Date will come directly from POST as YYYY-MM-DD
        appointment_date = datetime.strptime(request.POST['date'], "%Y-%m-%d").date()
        time_slot = time.fromisoformat(request.POST['time'])

        # Prevent double booking
        if Appointment.objects.filter(date=appointment_date, time=time_slot).exists():
            return redirect(f'/book_appointment/?date={appointment_date}')

        Appointment.objects.create(
            user=request.user,
            name=name,
            age=age,
            email=email,
            phone=phone,
            date=appointment_date,
            time=time_slot,
            status="Pending"
        )
        return redirect('my_appointments')

    return render(
        request,
        "book_appointment.html",
        {"slots": slots, "selected_date": selected_date}
    )






@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(user=request.user).order_by("-date", "-time")
    return render(request, "my_appointments.html", {"appointments": appointments})


@login_required
def delete_appointment(request, id):
    appointment = Appointment.objects.get(id=id, user=request.user)
    appointment.delete()
    
    return redirect('my_appointments')










"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('about',views.about,name='about'),
    path('services',views.services,name='services'),
    path('blog',views.blog,name='blog'),
   
    path('blog_details',views.blog_details,name='blog_details'),
    path('contact',views.contact,name='contact'),
    path('elements',views.elements,name='elements'),
    path('register',views.register,name='register'),
    path('login',views.Login,name='login'),
    path('loginindex',views.loginindex,name='loginindex'),
     path('logout/', views.user_logout, name='logout'),
     path('profile',views.profile,name='profile'),
     path('loginabout',views.loginabout,name='loginabout'),
     path('loginservices',views.loginservices,name='loginservices'),
     path('logincontact',views.logincontact,name='logincontact'),
     path('profileedit',views.edit,name='profileedit'),
     path('password_reset',views.password_reset_request,name='password_reset'),
     path('verify_otp',views.verify_otp,name='verify_otp'),
     path('set_new_password',views.set_new_password,name='set_new_password'),
]

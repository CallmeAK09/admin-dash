from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,aauthenticate
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

@never_cache
def signup_view(request):
    error = {
        'username' : '',
        'email' : '',
        'password1' : '',
        'password2' : '',
    }
    has_error= False
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username:
            error['username'] = "Enter username."
            has_error = True
        elif len(username) < 3 or len(username) > 8:
            error['username'] = "User name must have 3-8 characters."
            has_error = True
        elif User.objects.filter(username = username).exists():
            error['username'] = "User exist."
            has_error = True
        elif not email:
            error['email'] = "Enter email."
            has_error = True
        elif '@' not in email or '.' not in email:
            error['email'] = "Enter a vlaid email."
            has_error = True
        elif User.objects.filter(email = email).exists():
            error['email'] = "Email exist."
            has_error = True
        elif not password1 :
            error['password1'] = "Enter passowrd."
            has_error = True
        elif len(password1)<6:
            error['password1'] = "Password lenth is 6."
            has_error = True
        elif not password2 :
            error['password2'] = "Confirm password."
            has_error = True
        elif password1 != password2:
            error['password2'] = "Passwords not match."

            has_error = True
        
        if not has_error:
            user = User.objects.create_user(username = username , email = email , password = password1)
            login(request,user)
            return redirect('home')
    return render(request,'signup.html',{'error':error})

@never_cache
def login_view(request):
    if request.session:
        redirect('home')
    error = ''
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        if not user_id or not password:
            error = 'Enter fields.'
        else:
            user = ( User.objects.filter(username = user_id ).first() or User.objects.filter(email = user_id).first() )

            if user and user.check_password(password):
                
                login(request,user)
                return redirect('home')
            
            else:
                error = 'No user found Chek username or password'

    return render(request,'login.html',{'error' : error})

@never_cache
@login_required(login_url='login')
def home_view(request):
    
    greet = 'welcome'
    name = request.user.username
    return render(request,'index.html',{'greet':greet,'name':name})

@never_cache
def logout_view(request):
    logout(request)
    return redirect('login')

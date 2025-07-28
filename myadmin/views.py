from django.shortcuts import render,redirect
from  django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required


# Create your views here.
@never_cache
def admin_login_view(request):
    error=''
    if request.method=='POST':
        admin_id = request.POST.get('admin_id').strip()
        admin_pass = request.POST.get('admin_pass').strip()

        if not admin_id or not admin_pass:
            error = 'Enter fields.'
        else:
            user = ( User.objects.filter(username = admin_id ).first() or User.objects.filter(email = admin_id).first() )

            if user and user.check_password(admin_pass) and user.is_superuser:

                login(request,user)
                return redirect('myadmin_home')
            
            else:
                error = 'No user found.Check username or password'
    return render(request,'admin_login.html',{'error':error})

# Home
@never_cache
@login_required(login_url='myadmin')
def admin_home_view(request):
    
    return render(request,'admin_home.html')

# Logout
@never_cache
def admin_logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('myadmin')

# List
@never_cache
def admin_user_list_view(request):
    users = User.objects.filter(is_staff=False)

    return render(request,'admin_user_list.html',{'users':users})

# Edit
@never_cache
def admin_user_edit_view(request, id):
    user = User.objects.filter(id=id, is_superuser=False).first()
    if not user:
        return redirect('myadmin_users')

    error = ''
    success = ''

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username:
            error = 'Username is required.'
        elif len(username) < 3 or len(username) > 8:
            error = 'Username must be between 3 and 8 characters.'
        elif User.objects.exclude(id=id).filter(username=username).exists():
            error = 'Username already exists.'
        else:
            user.username = username
            if password:
                if len(password) < 6:
                    error = 'Password must be at least 6 characters.'
                else:
                    user.set_password(password)
            if not error:
                user.save()
                return redirect('myadmin_users')

    return render(request, 'admin_edit_user.html', {'user': user,'error': error,})

# Delete
@never_cache
def admin_delete_user_view(request, id):
    if request.method=='POST':
        user=User.objects.filter(id=id,is_superuser=False).first()
        if user:
            user.delete()

    return redirect('myadmin_users')

# Create
@never_cache
def admin_user_create_view(request):
    
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
            return redirect('myadmin_users')
        
    return render(request,'admin_create_user.html',{'error':error})

@never_cache
def admin_logout_view(request):
    logout(request)
    return redirect('myadmin')

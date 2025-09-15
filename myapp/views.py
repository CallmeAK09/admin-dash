from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from .signals import manual_signal


# Helper to check if user is logged in using session
def is_user_logged(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    return None


# Signup
@method_decorator(never_cache, name='dispatch')
class SignupView(View):
    template_name = 'signup.html'

    def get(self, request):
        if is_user_logged(request):
            return redirect('home')
        error = {'username': '', 'email': '', 'password1': '', 'password2': ''}
        return render(request, self.template_name, {'error': error})

    def post(self, request):
        if is_user_logged(request):
            return redirect('home')

        error = {'username': '', 'email': '', 'password1': '', 'password2': ''}
        has_error = False

        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Username validation
        if not username:
            error['username'] = "Enter username."
            has_error = True
        elif len(username) < 3 or len(username) > 8:
            error['username'] = "User name must have 3-8 characters."
            has_error = True
        elif User.objects.filter(username=username).exists():
            error['username'] = "User exists."
            has_error = True

        # Email validation
        if not email:
            error['email'] = "Enter email."
            has_error = True
        elif '@' not in email or '.' not in email:
            error['email'] = "Enter a valid email."
            has_error = True
        elif User.objects.filter(email=email).exists():
            error['email'] = "Email exists."
            has_error = True

        # Password validation
        if not password1:
            error['password1'] = "Enter password."
            has_error = True
        elif len(password1) < 6:
            error['password1'] = "Password must be at least 6 characters."
            has_error = True

        if not password2:
            error['password2'] = "Confirm password."
            has_error = True
        elif password1 != password2:
            error['password2'] = "Passwords do not match."
            has_error = True

        
        if not has_error:
            user = User.objects.create_user(username=username, email=email, password=password1)
            request.session['user_id'] = user.id
            request.session.set_expiry(3600)
            return redirect('home')

        return render(request, self.template_name, {'error': error})


# Login
@method_decorator(never_cache, name='dispatch')
class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        if is_user_logged(request):
            return redirect('home')
        return render(request, self.template_name, {'error': ''})

    def post(self, request):
        if is_user_logged(request):
            return redirect('home')

        error = ''
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        if not user_id or not password:
            error = 'Enter fields.'
        else:
            user = (
                User.objects.filter(username=user_id).first()
                or User.objects.filter(email=user_id).first()
            )

            if user and user.check_password(password):
                request.session['user_id'] = user.id
                request.session.set_expiry(3600)
                
                # custom signaling
                manual_signal.send(sender = None, user = user)
                
                return redirect('home')
            else:
                error = 'No user found. Check username or password.'

        return render(request, self.template_name, {'error': error})


# Home
@method_decorator(never_cache, name='dispatch')
class HomeView(View):
    def get(self, request):
        user = is_user_logged(request)
        if not user:
            return redirect('login')
        greet = 'welcome'
        name = user.username
        return render(request, 'index.html', {'greet': greet, 'name': name})

# Logout
@method_decorator(never_cache, name='dispatch')
class LogoutView(View):
    def get(self, request):
        request.session.flush() 
        return redirect('login')

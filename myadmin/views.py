from django.shortcuts import render,redirect,get_object_or_404
from  django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views import View
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# To check admin logged in
def is_admin_logged_in(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        try:
            return User.objects.get(id=admin_id)
        except User.DoesNotExist:
            return None
    return None


# Create your views here.
@method_decorator(never_cache,name='dispatch')
class AdminLoginView(View):
    
    def get(self,request):

        if is_admin_logged_in(request):
            return redirect('myadmin_home')
        
        return render(request,'admin_login.html')

    def post(self,request):
        
        if is_admin_logged_in(request):
            return redirect('myadmin_home')

        error=''

        admin_id = request.POST.get('admin_id').strip()
        admin_pass = request.POST.get('admin_pass').strip()

        if not admin_id or not admin_pass:
            error = 'Enter fields.'
        else:
            user = ( User.objects.filter(username = admin_id ).first() or User.objects.filter(email = admin_id).first() )

            if user and user.check_password(admin_pass) and user.is_superuser:
                request.session['admin_id'] = user.id
                return redirect('myadmin_home')
            
            else:
                error = 'No user found.Check username or password'

        return render(request,'admin_login.html',{'error':error})

# Home
@method_decorator(never_cache,name='dispatch')
class AdminHomeView(View):

    def get(self,request):

        if not is_admin_logged_in(request):
            return redirect('myadmin')
    
        return render(request,'admin_home.html')

# Logout
@method_decorator(never_cache,name='dispatch')
class AdminLogoutView(View):

    def get(self,request):
        
        if 'admin_id' in request.session:
            del request.session['admin_id']

        return redirect('myadmin')

# List
@method_decorator(never_cache,name='dispatch')
class AdminUserListView(View):

    def get(self,request):

        if not is_admin_logged_in(request):
            return redirect('myadmin')
        
        query = request.GET.get('q', '').strip()

        if query:
            users = User.objects.filter(
                Q(username__icontains=query) | Q(email__icontains=query),
                is_superuser=False
                )
        else:
            users = User.objects.filter(is_superuser=False)

        return render(request, 'admin_user_list.html', {'users': users})

# Edit
@method_decorator(never_cache,name='dispatch')
class AdminEditView(View):
    def get(self,request,id):

        if not is_admin_logged_in(request):
            return redirect('myadmin')
        
        user = get_object_or_404(User, id=id, is_superuser=False)

        return render(request, 'admin_edit_user.html', {'user': user,})
    
    def post(self,request,id):

        if not is_admin_logged_in(request):
            return redirect('myadmin')

        user     = get_object_or_404(User, id=id, is_superuser=False)

        error    = ''

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
@method_decorator(never_cache,name='dispatch')
class AdminDeleteView(View):
    def get(self,request,id):

        if not is_admin_logged_in(request):
            return redirect('myadmin')

        user = get_object_or_404(User, id=id, is_superuser=False)
        
        return render(request,'admin_delete_confirm.html',{'user':user})
    
    def post(self,request, id):
        if not is_admin_logged_in(request):
            return redirect('myadmin')
        
        user=get_object_or_404(User, id=id,is_superuser=False)
        user.delete()

        return redirect('myadmin_users')
    
# create
@method_decorator(never_cache, name='dispatch')
class AdminCreateView(View):
    def get(self, request):

        if not is_admin_logged_in(request):
            return redirect('myadmin')

        error = {'username': '', 'email': '', 'password1': ''}
        return render(request, 'admin_create_user.html', {'error': error})

    def post(self, request):

        admin = is_admin_logged_in(request)
        if not admin or not admin.is_superuser:
            return redirect('myadmin')


        error = {
            'username': '',
            'email': '',
            'password1': '',
        }
        has_error = False

        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '').strip()

        # --- Validation ---
        if not username:
            error['username'] = "Enter username."
            has_error = True
        elif len(username) < 3 or len(username) > 8:
            error['username'] = "Username must be 3–8 characters."
            has_error = True
        elif User.objects.filter(username=username).exists():
            error['username'] = "User already exists."
            has_error = True

        if not email:
            error['email'] = "Enter email."
            has_error = True
        elif '@' not in email or '.' not in email:
            error['email'] = "Enter a valid email."
            has_error = True
        elif User.objects.filter(email=email).exists():
            error['email'] = "Email already exists."
            has_error = True

        if not password1:
            error['password1'] = "Enter password."
            has_error = True
        elif len(password1) < 6:
            error['password1'] = "Password must be at least 6 characters."
            has_error = True

        if not has_error:
            User.objects.create_user(username=username, email=email, password=password1)
            return redirect('myadmin_users')

        return render(request, 'admin_create_user.html', {'error': error})

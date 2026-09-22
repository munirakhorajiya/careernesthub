from django.shortcuts import render,redirect
from .models import User
from .models import ServiceProvider
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout
from functools import wraps
# Create your views here.

def admin_required(view_func):
    # Only admin (Django staff/superuser + session flag) can open
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and (request.user.is_staff or request.user.is_superuser)
            and request.session.get('account_type') == 'admin'
        ):
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return wrapper

def register(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        phone=request.POST['phone']
        account_type=request.POST['account_type']

        if account_type=="user":
            if User.objects.filter(email=email).exists():
                return render(request,'accounts/register.html',{'error':'email already registerd'})
            User.objects.create(
                name=name,
                email=email,
                password=password,
                phone=phone,
            )

        elif account_type=='provider':
            company_name=request.POST.get('company_name','')
            description=request.POST.get('description','')
            address=request.POST.get('address','')

            if ServiceProvider.objects.filter(email=email).exists():
                return render(request,'accounts/register.html',{'error':'email already registerd'})

            ServiceProvider.objects.create(
                name=name,
                email=email,
                password=password,
                phone=phone,
                company_name=company_name,
                address=address,
                description=description
            )

        return redirect('login')    
    return render(request,'accounts/register.html')

def login(request):

    if request.method=="POST":

        login_id=request.POST.get('email','').strip()  # email for user/provider, username for admin
        password=request.POST.get('password','')
        account_type=request.POST.get('account_type','')

        if account_type=="user":

            try:
                user=User.objects.get(
                    email=login_id,
                    password=password
                )
                request.session['user_id']=user.id
                request.session['account_type']='user'

                return redirect('user_profile')
            except User.DoesNotExist:

                return render(request,'accounts/login.html',{'error':'invalid email or password'})

        elif account_type=="provider":

            try:
                provider=ServiceProvider.objects.get(
                    email=login_id,
                    password=password
                )
                request.session['provider_id']=provider.id
                request.session['account_type']='provider'

                return redirect('provider_profile')

            except ServiceProvider.DoesNotExist:
                return render(request,'accounts/login.html',{'error':'invalid email or password'})

        elif account_type=='admin':
            # Admin uses Django username (not email)
            user=authenticate(request,username=login_id,password=password)
            if user and (user.is_staff or user.is_superuser):
                auth_login(request,user)
                request.session['account_type'] ='admin'
                return redirect('admin_dashboard')
            else:
                return render(request,'accounts/login.html',{'error':'invalid admin'})

    return render(request,'accounts/login.html')

@admin_required
def admin_dashboard(request):
    # Only admin can open - others redirected to login by decorator
    context = {
        'user_count': User.objects.count(),
        'provider_count': ServiceProvider.objects.count(),
    }
    return render(request, 'accounts/admin_dashboard.html', context)

def user_profile(request):

    if 'user_id' not in request.session or request.session.get('account_type') != 'user':
        return redirect('login')

    user=User.objects.get(
        id=request.session['user_id']
    )

    return render(request,'accounts/user_profile.html',{'user':user})

def provider_profile(request):

    if 'provider_id' not in request.session or request.session.get('account_type') != 'provider':
        return redirect('login')

    provider=ServiceProvider.objects.get(
        id=request.session['provider_id']
    )

    return render(request,'accounts/provider_profile.html',{'provider':provider})

@admin_required
def user_list(request):
    name=request.GET.get('name','')

    users=User.objects.filter(
        name__icontains=name
    )

    return render(request,'accounts/user_list.html',{'users':users,'name':name})

@admin_required
def provider_list(request):
    name=request.GET.get('name','')

    providers=ServiceProvider.objects.filter(
        name__icontains=name
    )

    return render(request,'accounts/provider_list.html',{'providers':providers,'name':name})
               

def logout(request):
    auth_logout(request)
    request.session.flush()
    return redirect('login')
    

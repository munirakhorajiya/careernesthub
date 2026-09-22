from django.shortcuts import render,redirect
from accounts.models import User,ServiceProvider
from .models import Cource,Enrollmentno
# Create your views here.

def cource_detail(request,id):
    if 'user_id' not in request.session and 'provider_id' not in request.session:
        return redirect('login')
    cource=Cource.objects.get(id=id)
    return render(request,'cources/cource_detail.html',{'cource':cource})

def cource_list(request):
    if 'user_id' not in request.session and 'provider_id' not in request.session:
        return redirect('login')
    cource=Cource.objects.all()
    return render(request,'cources/cource_list.html',{'cource':cource})

def cource_create(request):
    if 'provider_id' not in request.session:
        return redirect('login')

    provider=ServiceProvider.objects.get(id=request.session['provider_id'])

    if request.method=='POST':
        Cource.objects.create(
            provider=provider,  
            title=request.POST['title'],
            price=request.POST['price'],
            duration=request.POST['duration'],
        )
        return redirect('cource_list')
    return render(request,'cources/cource_create.html')

def my_cource(request):
    if 'provider_id' not in request.session:
        return redirect('login')

    provider=ServiceProvider.objects.get(id=request.session['provider_id'])

    cource=Cource.objects.filter(provider=provider)
    return render(request,'cources/my_cource.html',{'cource':cource})

def cource_enroll(request,id):
    if 'user_id' not in request.session or request.session.get('account_type') != 'user':
        return redirect('login')

    user=User.objects.get(id=request.session['user_id'])

    cource=Cource.objects.get(id=id)

    Enrollmentno.objects.get_or_create(user=user,cource=cource)

    return redirect('my_enrollment')

def my_enrollment(request):
    if 'user_id' not in request.session:
        return redirect('login')
    user=User.objects.get(id=request.session['user_id'])
    enroll=Enrollmentno.objects.filter(user=user)
    return render(request,'cources/my_enrollment.html',{'enroll':enroll})


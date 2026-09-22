from django.shortcuts import render,redirect
from django.db.models import Q as models_Q
from .models import Job,Internship,Application
from accounts.models import User,ServiceProvider

# Create your views here.


def job_list(request):
    if 'user_id' not in request.session and 'provider_id' not in request.session:
        return redirect('login')
    jobs=Job.objects.all()

    return render(request,'opportunities/job_list.html',{'jobs':jobs})

def job_details(request,id):
    if 'user_id' not in request.session and 'provider_id' not in request.session:
        return redirect('login')
    job=Job.objects.get(id=id)

    return render(request,'opportunities/job_details.html',{'job':job})

def job_create(request):
    if 'provider_id' not in request.session:
        return redirect('login')

    provider=ServiceProvider.objects.get(id=request.session['provider_id'])

    if request.method=='POST':
        title=request.POST['title']
        description=request.POST['description']
        location=request.POST['location']
        salary=request.POST['salary']
        skills=request.POST['skills']

        Job.objects.create(
            title=title,
            description=description,
            provider=provider,
            location=location,
            salary=salary,
            skills=skills
        )

        return redirect('job_list')
    return render(request,'opportunities/job_create.html')

def job_delete(request, id):
    if 'provider_id' not in request.session or request.session.get('account_type') != 'provider':
        return redirect('login')
    try:
        job = Job.objects.get(id=id, provider_id=request.session['provider_id'])
    except Job.DoesNotExist:
        return redirect('job_list')
    job.delete()
    return redirect('job_list')

def internship_list(request):
    if 'user_id' not in request.session and 'provider_id' not in request.session:
        return redirect('login')
    internship=Internship.objects.all()
    return render(request,'opportunities/internship_list.html',{'internship':internship})

def internship_details(request, id):
    if 'user_id' not in request.session and 'provider_id' not in request.session:
        return redirect('login')
    internship=Internship.objects.get(id=id)

    return render(request,'opportunities/internship_details.html',{'internship':internship})

def internship_create(request):

    if 'provider_id' not in request.session:
        return redirect('login')

    provider=ServiceProvider.objects.get(id=request.session['provider_id'])

    if request.method=="POST":
        Internship.objects.create(
            provider=provider,
            title=request.POST['title'],
            description=request.POST['description'],
            location=request.POST['location'],
            stipend=request.POST['stipend'],
            duration=request.POST['duration'],
            skills=request.POST['skills']
        )
        return redirect('internship_list')
    return render(request,'opportunities/internship_create.html')

def job_apply(request, id):

    if 'user_id' not in request.session or request.session.get('account_type') != 'user':
        return redirect('login')
    
    user=User.objects.get(id=request.session['user_id'])

    job=Job.objects.get(id=id)

    if Application.objects.filter(user=user,job=job).exists():
        return redirect('application_list')
    
    Application.objects.create(
        user=user,
        job=job
    )
    return redirect('application_list')
    

def internship_apply(request, id):

    if 'user_id' not in request.session or request.session.get('account_type') != 'user':
        return redirect('login')

    user=User.objects.get(id=request.session['user_id'])

    internship=Internship.objects.get(id=id)

    if Application.objects.filter(user=user,internship=internship).exists():
        return redirect('application_list')
    
    Application.objects.create(
        user=user,
        internship=internship
    )
    return redirect('application_list')
    

def application_list(request):

    if 'user_id' not in request.session:
        return redirect('login')

    user=User.objects.get(id=request.session['user_id'])

    application=Application.objects.filter(
        user=user
    )

    return render(request,'opportunities/application_list.html',{'application':application})

def provider_applications(request):
    if 'provider_id' not in request.session:
        return redirect('login')
    pid = request.session['provider_id']
    applications = Application.objects.filter(
        models_Q(job__provider_id=pid) | models_Q(internship__provider_id=pid)
    ).order_by('-applied_date')
    return render(request, 'opportunities/provider_applications.html', {'applications': applications})


def update_status(request, id, action):
    if 'provider_id' not in request.session:
        return redirect('login')
    pid = request.session['provider_id']
    app = Application.objects.get(id=id)
    # security: only owner provider can update
    is_owner = (app.job and app.job.provider_id == pid) or (app.internship and app.internship.provider_id == pid)
    if not is_owner:
        return redirect('login')
    if action in ['Accepted', 'Rejected', 'Pending','Completed']:
        app.status = action
        app.save()
    return redirect('provider_applications')
    
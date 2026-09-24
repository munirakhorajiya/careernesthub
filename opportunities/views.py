from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q as models_Q
from .models import Job,Internship,Application
from accounts.models import User,ServiceProvider
from django.http import FileResponse,Http404

# Create your views here.


def job_list(request):
    # Public list - anyone (guest, user, provider, admin) can see
    jobs=Job.objects.all().order_by('-id')

    return render(request,'opportunities/job_list.html',{'jobs':jobs})

def job_details(request,id):
    # Public detail - template already shows Login to Apply for guests
    job=get_object_or_404(Job,id=id)

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
    # Public list - anyone can see
    internship=Internship.objects.all().order_by('-id')
    return render(request,'opportunities/internship_list.html',{'internship':internship})

def internship_details(request, id):
    # Public detail
    internship=get_object_or_404(Internship,id=id)

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

def upload_certificate(request,id):
    if 'provider_id' not in request.session:
        return redirect('login')
    pid=request.session['provider_id']
    try:
        app=Application.objects.select_related('user','job','internship').get(id=id)
    except Application.DoesNotExist:
        return redirect('provider_applications')
    is_owner=(app.job and app.job.provider_id==pid) or (app.internship and app.internship.provider_id==pid)
    if not is_owner:
        return redirect('login')
    if app.status != 'Completed':
        return redirect('provider_applications')
    error = None
    if request.method=='POST':
        f = request.FILES.get('certificate')
        if not f:
            error = 'Please choose a file to upload.'
        else:
            valid_types = ('image/jpeg', 'image/png', 'image/webp', 'application/pdf')
            if f.content_type not in valid_types and not f.name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.pdf')):
                error = 'Only JPG, PNG, WEBP images or PDF allowed.'
            elif f.size > 5 * 1024 * 1024:
                error = 'File too large. Max 5 MB allowed.'
            else:
                if app.certificate:
                    app.certificate.delete(save=False)
                app.certificate=f
                app.save()
                return redirect('provider_applications')
    return render(request,'opportunities/upload_certificate.html',{'app':app, 'error': error})

def download_certificate(request,id):
    try:
        app=Application.objects.get(id=id)
    except Application.DoesNotExist:
        raise Http404('no certificate')
    if not app.certificate:
        raise Http404('no certificate')
    user_id=request.session.get('user_id')
    provider_id=request.session.get('provider_id')
    is_user_owner=user_id and app.user_id == user_id
    is_provider_owner=provider_id and ((app.job and app.job.provider_id == provider_id)or(app.internship and app.internship.provider_id==provider_id))
    if not (is_user_owner or is_provider_owner):
        return redirect('login')
    if app.status != 'Completed':
        raise Http404("not completed")
    import os
    filename = os.path.basename(app.certificate.name)
    return FileResponse(app.certificate.open('rb'), as_attachment=True, filename=filename)


from django.urls import path
from . import views

urlpatterns = [
    path('jobs/',views.job_list,name='job_list'),
    path('jobs/<int:id>/',views.job_details,name='job_details'),
    path('job/create/',views.job_create,name='job_create'),
    path('job/<int:id>/delete/',views.job_delete,name='job_delete'),
    path('internship/',views.internship_list,name='internship_list'),
    path('internship/<int:id>/',views.internship_details,name='internship_details'),
    path('internship/create/',views.internship_create,name='internship_create'),
    path('job/<int:id>/apply/',views.job_apply,name='job_apply'),
    path('internship/<int:id>/apply/',views.internship_apply,name='internship_apply'),
    path('application/',views.application_list,name='application_list'),
    path('provider/applications/',views.provider_applications,name='provider_applications'),
    path('application/<int:id>/<str:action>/',views.update_status,name='update_status'),
]
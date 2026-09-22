from django.urls import path
from . import views

urlpatterns = [
    path('', views.cource_list, name='cource_list'),
    path('<int:id>/', views.cource_detail, name='cource_detail'),
    path('create/', views.cource_create, name='cource_create'),
    path('my/', views.my_cource, name='my_cource'),
    path('<int:id>/enroll/', views.cource_enroll, name='cource_enroll'),
    path('my-enrollment/', views.my_enrollment, name='my_enrollment'),
]
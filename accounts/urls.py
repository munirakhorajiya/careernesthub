from django.urls import path
from . import views

urlpatterns = [
    path('',views.register,name='register'),
    path('login/',views.login,name='login'),

    path('user_profile/',views.user_profile,name='user_profile'),
    path('user_profile/edit/',views.user_profile_edit,name='user_profile_edit'),
    path('provider-profile/', views.provider_profile, name='provider_profile'),

    path('users/', views.user_list, name='user_list'),
    path('providers/', views.provider_list, name='provider_list'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('logout/', views.logout, name='logout'),
]

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('edit_form/<int:form_id>/', views.edit_form, name='edit_form'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='pds_app/login.html'), name='login'),
    path('form/<str:section>/', views.section_view, name='section_view'),
    path('', views.home, name='home'),
    path('create_form/', views.create_form, name='create_form'),
    path('forms/', views.forms, name='forms'),
    path('all_forms/<int:form_id>', views.all_forms, name='all_forms'),
    path('delete_form/<int:form_id>', views.delete_form, name='delete_form'),
]
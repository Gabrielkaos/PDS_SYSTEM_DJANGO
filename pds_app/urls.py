
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('form/create_form/', views.create_form, name='create_form'),
    path('form/edit_form/<int:form_id>/', views.edit_form, name='edit_form'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='pds_app/login.html'), name='login'),
    path('', views.home, name='home'),
    path('forms/<int:form_id>', views.all_forms, name='all_forms'),
    path('delete_form/<int:form_id>', views.delete_form, name='delete_form'),
]
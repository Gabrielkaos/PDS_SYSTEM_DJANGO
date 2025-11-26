
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('form/import_form/', views.import_multiple_forms, name='import_form'),
    path('form/export/<int:form_id>/', views.export_form, name='export_form'),
    path('form/create_form/', views.create_form, name='create_form'),
    path('form/edit_form/<int:form_id>/', views.edit_form, name='edit_form'),
    
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='pds_app/login.html'), name='login'),
    
    path('', views.home, name='home'),
    path('forms/<int:form_id>', views.all_forms, name='all_forms'),
    path('delete_form/<int:form_id>', views.delete_form, name='delete_form'),

    path('bulk-delete/', views.bulk_delete_forms, name='bulk_delete'),
    path('bulk-export/', views.bulk_export_forms, name='bulk_export'),
    path('import-multiple/', views.import_multiple_forms, name='import_multiple'),
]
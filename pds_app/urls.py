
from django.urls import path
from . import views


urlpatterns = [
    path('form/<str:section>/', views.section_view, name='section_view'),
    path('', views.home, name='home'),
    path('create_form/', views.create_form, name='create_form'),
    path('forms/', views.forms, name='forms'),
    path('all_forms/<int:form_id>', views.all_forms, name='all_forms')
]
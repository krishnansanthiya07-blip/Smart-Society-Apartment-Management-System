from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('resident-login/', views.resident_login, name='resident_login'),
    path('resident-dashboard/', views.resident_dashboard, name='resident_dashboard'),
    path('resident-profile/', views.resident_profile, name='resident_profile'),
    path('apartment-details/', views.apartment_details, name='apartment_details'),
    path('payments/', views.payments, name='payments'),
    path('complaints/', views.complaints, name='complaints'),
    path('add-complaint/', views.add_complaint, name='add_complaint'),
    path('maintenance/', views.maintenance, name='maintenance'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
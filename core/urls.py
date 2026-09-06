from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('resident-login/', views.resident_login, name='resident_login'),
    path('resident-dashboard/', views.resident_dashboard, name='resident_dashboard'),
    path('resident-profile/', views.resident_profile, name='resident_profile'),
    path('apartment-details/',views.apartment_details,name='apartment_details'),
]
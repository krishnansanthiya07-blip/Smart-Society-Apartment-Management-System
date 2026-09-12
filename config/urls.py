"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to 
    urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns= [
    path('admin/',admin.site.urls),
    path('',views.home,name='home'),
    path('resident-login/',views.resident_login,name='resident_login'),
    path('resident-dashboard/',views.resident_dashboard,name='resident_dashboard'),
    path('resident-profile/',views.resident_profile,name='resident_profile'),
    path('apartment-details/',views.apartment_details,name='apartment_details'),
    path('payments/',views.payments,name='payments'),
    path('complaints/',views.complaints,name='complaints'),
    path('add-complaint/',views.add_complaint,name='add_complaint'),
    path('maintenance/',views.maintenance,name='maintenance'),
]
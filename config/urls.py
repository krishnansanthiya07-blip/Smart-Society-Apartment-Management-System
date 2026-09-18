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
    path('admin-login/',views.admin_login,name='admin_login'),
    path('admin-dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('manage-residents/',views.manage_residents,name='manage_residents'),
    path('manage-apartments/',views.manage_apartments,name='manage_apartments'),
    path('admin-payments/',views.admin_payments,name='admin_payments'),
    path('admin-complaints/',views.admin_complaints,name='admin_complaints'),
    path('update-complaint-status/<int:complaint_id>/',views.update_complaint_status,name='update_complaint_status'),
    path('admin-maintenance/',views.admin_maintenance,name='admin_maintenance'),
    path('add-maintenance-member/',views.add_maintenance_member,name='add_maintenance_member'), 
    path('edit-maintenance-member/<int:member_id>/',views.edit_maintenance_member,name='edit_maintenance_member'),
    path('delete-maintenance-member/<int:member_id>/',views.delete_maintenance_member,name='delete_maintenance_member'),
    path('assign-complaint/<int:complaint_id>/',views.assign_complaint,name='assign_complaint'),
    path('admin-logout/',views.admin_logout,name='admin_logout'),
    path('resident-logout/',views.resident_logout,name='resident_logout'),
    path('maintenance-login/',views.maintenance_login,name='maintenance_login'),
    path('maintenance-dashboard/',views.maintenance_dashboard,name='maintenance_dashboard'),
    path('update-maintenance-status/<int:complaint_id>/',views.update_maintenance_status,name='update_maintenance_status'),
    path('maintenance-logout/',views.mainteneance_logout,name='maintenance_logout'),
]  


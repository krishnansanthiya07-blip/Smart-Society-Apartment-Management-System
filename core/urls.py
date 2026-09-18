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

    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-residents/', views.manage_residents, name='manage_residents'),
    path('manage-apartments/', views.manage_apartments, name='manage_apartments'),
    path('admin-payments/', views.admin_payments, name='admin_payments'),
    path('admin-complaints/', views.admin_complaints, name='admin_complaints'),

    path('update-complaint-status/<int:complaint_id>/', views.update_complaint_status, name='update_complaint_status'),
    path('assign-complaint/<int:complaint_id>/', views.assign_complaint, name='assign_complaint'),

    path('admin-maintenance/', views.admin_maintenance, name='admin_maintenance'),
    path('add-maintenance-member/', views.add_maintenance_member, name='add_maintenance_member'),
    path('edit-maintenance-member/<int:member_id>/', views.edit_maintenance_member, name='edit_maintenance_member'),
    path('delete-maintenance-member/<int:member_id>/', views.delete_maintenance_member, name='delete_maintenance_member'),

    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('resident-logout/', views.resident_logout, name='resident_logout'),
]
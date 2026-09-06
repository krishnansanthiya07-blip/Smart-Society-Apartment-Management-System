from django.shortcuts import render
from .models import Resident,Apartment,Payment,Complaint,MaintenanceTeam

def home(request):
    return render(request,'core/home.html')
def resident_login(request):
    return render(request,'core/resident_login.html')
def resident_dashboard(request):
    resident=Resident.objects.first()
    return render(request,'core/resident_dashboard.html',{'resident':resident})
def resident_profile(request):
    resident=Resident.objects.first()
    apartment=Apartment.objects.get(apartment_number=resident.apartment)
    return render(request,'core/resident_profile.html',{'resident':resident,'apartment':apartment})
def apartment_details(request):
    return render(request,'core/apartment_details.html')
def payments(request):
    resident=Resident.objects.first()
    payments=Payment.objects.filter(resident=resident)
    return render(request,'core/payments.html',{'resident':resident,'payments':payments})
def complaints(request):
    resident = Resident.objects.first()
    complaints = Complaint.objects.filter(resident=resident)

    return render(request, 'core/complaints.html', {
        'resident': resident,
        'complaints': complaints
    })
def maintenance(request):
    teams = MaintenanceTeam.objects.all()
    return render(request,'core/maintenance.html',{'teams':teams})


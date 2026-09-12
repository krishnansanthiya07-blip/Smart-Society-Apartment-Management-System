from django.shortcuts import render,redirect
from .models import Resident,Apartment,Payment,Complaint,MaintenanceTeam

def home(request):
    return render(request,'core/home.html')
def resident_login(request):
    return render(request,'core/resident_login.html')
def resident_dashboard(request):
    resident = Resident.objects.first()

    complaints = Complaint.objects.filter(resident=resident)
    total_complaints = complaints.count()
    pending_complaints = complaints.filter(status='Pending').count()

    return render(request, 'core/resident_dashboard.html', {
        'resident': resident,
        'total_complaints': total_complaints,
        'pending_complaints': pending_complaints
    })
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
def add_complaint(request):
    resident = Resident.objects.first()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        Complaint.objects.create(
            resident=resident,
            title=title,
            description=description,
            status='Pending'
        )

        return redirect('complaints')

    return render(request, 'core/add_complaint.html')
def maintenance(request):
    teams = MaintenanceTeam.objects.all()
    return render(request,'core/maintenance.html',{'teams':teams})
def admin_dashboard(request):
    residents = Resident.objects.all().count()
    apartments = Apartment.objects.all().count()
    complaints = Complaint.objects.all().count()
    payments = Payment.objects.all().count()

    return render(request, 'core/admin_dashboard.html', {
        'residents': residents,
        'apartments': apartments,
        'complaints': complaints,
        'payments': payments
    })

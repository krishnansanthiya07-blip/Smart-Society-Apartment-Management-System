from django.shortcuts import render, redirect
from .models import Apartment, Resident, Payment, Complaint, MaintenanceTeam

def home(request):
    return render(request, 'core/home.html')


def resident_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'resident' and password == 'resident123':
            request.session['resident_logged_in'] = True
            return redirect('resident_dashboard')
    return render(request, 'core/resident_login.html')


def resident_dashboard(request):

    if not request.session.get("resident_logged_in"):
        return redirect('resident_login')

    resident = Resident.objects.first()

    if resident:
        total_complaints = Complaint.objects.filter(
            resident=resident
        ).count()

        pending_complaints = Complaint.objects.filter(
            resident=resident,
            status='Pending'
        ).count()
    else:
        total_complaints = 0
        pending_complaints = 0

    return render(request, 'core/resident_dashboard.html', {
        'total_complaints': total_complaints,
        'pending_complaints': pending_complaints
    })


def resident_profile(request):
    if not request.session.get("resident_logged_in"):
        return redirect('resident_login')


    resident = Resident.objects.first()

    return render(request, 'core/resident_profile.html', {
        'resident': resident
    })


def apartment_details(request):
    if not request.session.get("resident_logged_in"):
        return redirect('resident_login')
    resident = Resident.objects.first()

    return render(request, 'core/apartment_details.html', {
        'resident': resident
    })


def payments(request):
    if not request.session.get("admin_logged_in"):
        return redirect('admin_login')
    resident = Resident.objects.first()

    if resident:
        payment_list = Payment.objects.filter(resident=resident)
    else:
        payment_list = []

    return render(request, 'core/payments.html', {
        'payments': payment_list
    })


def complaints(request):
    if not request.session.get("resident_logged_in"):
        return redirect('resident_login')

    resident = Resident.objects.first()

    if resident:
        complaint_list = Complaint.objects.filter(resident=resident)
    else:
        complaint_list = []

    return render(request, 'core/complaints.html', {
        'complaints': complaint_list
    })


def add_complaint(request):
    if not request.session.get("resident_logged_in"):
        return redirect('resident_login')   
    resident = Resident.objects.first()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        if resident:
            Complaint.objects.create(
                resident=resident,
                title=title,
                description=description
            )

        return redirect('complaints')

    return render(request, 'core/add_complaint.html')


def maintenance(request):
    return render(request, 'core/maintenance.html')
def maintenance_login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')

        try:
            member = MaintenanceTeam.objects.get(
                name=name,
                phone=phone
            )
            request.session['maintenance_member_id'] = member.id
            return redirect('maintenance_dashboard')
        except MaintenanceTeam.DoesNotExist:
            pass

    return render(request, 'core/maintenance_login.html')


def maintenance_dashboard(request):
    member_id = request.session.get('maintenance_member_id')

    if not member_id:
        return redirect('maintenance_login')

    member = MaintenanceTeam.objects.get(id=member_id)

    assigned_complaints = Complaint.objects.filter(
        assigned_to=member
    )

    return render(request, 'core/maintenance_dashboard.html', {
        'member': member,
        'complaints': assigned_complaints
    })


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'admin' and password == 'admin123':
            request.session['admin_logged_in'] = True
            return redirect('admin_dashboard')
    return render(request, 'core/admin_login.html')



def admin_dashboard(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    total_residents = Resident.objects.count()
    total_apartments = Apartment.objects.count()
    total_complaints = Complaint.objects.count()
    total_payments = Payment.objects.count()

    return render(request, 'core/admin_dashboard.html', {
        'total_residents': total_residents,
        'total_apartments': total_apartments,
        'total_complaints': total_complaints,
        'total_payments': total_payments
    })


def manage_residents(request):
    if not request.session.get("admin_logged_in"):
        return redirect('admin_login')
    residents = Resident.objects.all()

    return render(request, 'core/manage_residents.html', {
        'residents': residents
    })


def manage_apartments(request):
    if not request.session.get("admin_logged_in"):
        return redirect('admin_login')
    apartments = Apartment.objects.all()

    return render(request, 'core/manage_apartments.html', {
        'apartments': apartments
    })


def admin_payments(request):
    if not request.session.get("admin_logged_in"):
        return redirect('admin_login')
    payments = Payment.objects.all()

    return render(request, 'core/admin_payments.html', {
        'payments': payments
    })


def admin_complaints(request):
    if not request.session.get("admin_logged_in"):
        return redirect('admin_login')
    complaints = Complaint.objects.all()
    maintenance_members = MaintenanceTeam.objects.all()

    return render(request, 'core/admin_complaints.html', {
        'complaints': complaints,
        'maintenance_members': maintenance_members
    })


def update_complaint_status(request, complaint_id):
    if not request.session.get("admin_logged_in"):
        return redirect('admin_login')
    complaint = Complaint.objects.get(id=complaint_id)

    if request.method == 'POST':
        complaint.status = request.POST.get('status')
        complaint.save()

    return redirect('admin_complaints')


def assign_complaint(request, complaint_id):
    if not request.session.get("admin_logged_in"):
        return redirect('admin_login')
    complaint = Complaint.objects.get(id=complaint_id)

    if request.method == 'POST':
        member_id = request.POST.get('assigned_to')

        if member_id:
            member = MaintenanceTeam.objects.get(id=member_id)
            complaint.assigned_to = member
        else:
            complaint.assigned_to = None

        complaint.save()

    return redirect('admin_complaints')

def admin_maintenance(request):
    if not request.session.get("admin_logged_in"):
        return redirect('admin_login')  
    teams = MaintenanceTeam.objects.all()

    return render(request, 'core/admin_maintenance.html', {
        'teams': teams
    })


def add_maintenance_member(request):
    if not request.session.get("admin_logged_in"):
        return redirect('admin_login')

    if request.method == 'POST':
        name = request.POST.get('name')
        role = request.POST.get('role')
        phone = request.POST.get('phone')

        MaintenanceTeam.objects.create(
            name=name,
            role=role,
            phone=phone
        )

        return redirect('admin_maintenance')

    return render(request, 'core/add_maintenance_member.html')


def edit_maintenance_member(request, member_id):
    if not request.session.get("admin_logged_in"):
        return redirect('admin_login')
    team = MaintenanceTeam.objects.get(id=member_id)

    if request.method == 'POST':
        team.name = request.POST.get('name')
        team.role = request.POST.get('role')
        team.phone = request.POST.get('phone')
        team.save()

        return redirect('admin_maintenance')

    return render(request, 'core/edit_maintenance_member.html', {
        'team': team
    })


def delete_maintenance_member(request, member_id):
    if not request.session.get("admin_logged_in"):
        return redirect('admin_login')
    team = MaintenanceTeam.objects.get(id=member_id)
    team.delete()

    return redirect('admin_maintenance')

def admin_logout(request):
    request.session.pop('admin_logged_in', None)
    return redirect('admin_login')

def resident_logout(request):
    request.session.flush()
    return redirect('resident_login')

def update_maintenance_status(request, complaint_id):
    member_id = request.session.get('maintenance_member_id')

    if not member_id:
        return redirect('maintenance_login')

    complaint = Complaint.objects.get(
        id=complaint_id,
        assigned_to_id=member_id
    )

    if request.method == 'POST':
        complaint.status = request.POST.get('status')
        complaint.save()

    return redirect('maintenance_dashboard')

def mainteneance_logout(request):
    request.session.pop('maintenance_member_id', None)
    return redirect('maintenance_login')
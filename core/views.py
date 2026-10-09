from django import core
from django.core.checks import messages
from django.http import request
from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Sum
from .models import Resident, Apartment , Payment, Complaint, MaintenanceTeam
from django.db import models
import random
from django.core.mail import send_mail
import requests
from django.conf import settings
from django.contrib import messages

def sign_up(request):
    return render(request,"core/sign_up.html")

def sign_in(request):
    if request.method == "POST":
        email = request.POST.get("email")

        otp = str(random.randint(100000, 999999))

        request.session["email"] = email
        request.session["otp"] = otp

        url = "https://api.brevo.com/v3/smtp/email"

        headers = {
            "accept": "application/json",
            "api-key": settings.BREVO_API_KEY,
            "content-type": "application/json",
        }

        data = {
            "sender": {
                "name": "Smart Society",
                "email": "krishnansanthiya07@gmail.com"
            },
            "to": [
                {
                    "email": email
                }
            ],
            "subject": "Smart Society - OTP",
            "htmlContent": f"<p>Your OTP is <strong>{otp}</strong></p>",
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code in [200, 201]:
            return redirect("otp_verification")

        return render(
            request,
            "core/sign_in.html",
            {"error": "Failed to send OTP."}
        )

    return render(request, "core/sign_in.html")


def home(request):
    return render(request, 'core/home.html')


def resident_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        try:
            resident = Resident.objects.get(
                email=email,
                phone=phone
            )

            request.session["resident_id"] = resident.id

            return redirect("resident_dashboard")

        except Resident.DoesNotExist:
            return render(request, "core/resident_login.html", {
                "error": "Invalid email or phone"
            })

    return render(request, "core/resident_login.html")

def resident_dashboard(request):

    if not request.session.get("resident_id"):
        return redirect('resident_login')

    resident_id=request.session.get("resident_id")
    resident = Resident.objects.get(id=resident_id)

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
        'resident': resident,   
        'total_complaints': total_complaints,
        'pending_complaints': pending_complaints
    })


def resident_profile(request):
    resident_id=request.session.get("resident_id")
    if not resident_id:
        return redirect('resident_login')

    resident = Resident.objects.get(id=resident_id)

    return render(request, "core/resident_profile.html", {
        'resident': resident
    })


def apartment_details(request):
    if not request.session.get("resident_id"):
        return redirect('resident_login')
    resident = Resident.objects.first()

    return render(request, 'core/apartment_details.html', {
        'resident': resident
    })

def payments(request):
    resident_id = request.session.get("resident_id")

    if not resident_id:
        return redirect("resident_login")

    resident = Resident.objects.get(id=resident_id)

    payment_list = Payment.objects.filter(
        resident=resident
    ).order_by("-payment_date")

    paid_amount = sum(
        payment.amount
        for payment in payment_list
        if payment.status == "PAID"
    )

    total_amount = resident.total_amount
    pending_amount = total_amount - paid_amount

    return render(request, "core/payments.html", {
        "resident": resident,
        "payments": payment_list,
        "total_amount": total_amount,
        "paid_amount": paid_amount,
        "pending_amount": pending_amount
    })
def make_payment(request):
    resident_id = request.session.get("resident_id")

    if not resident_id:
        return redirect("resident_login")

    resident = Resident.objects.get(id=resident_id)

    pending_amount = resident.total_amount - sum(
        payment.amount
        for payment in Payment.objects.filter(
            resident=resident,
            status="PAID"
        )
    )

    if pending_amount > 0:
        Payment.objects.create(
            resident=resident,
            amount=pending_amount,
            status="PAID"
        )

    return redirect("payments")


def complaints(request):
    resident_id = request.session.get("resident_id")

    if not resident_id:
        return redirect("resident_login")

    resident = Resident.objects.get(id=resident_id)

    complaint_list = Complaint.objects.filter(
        resident=resident
    )

    return render(request, "core/complaints.html", {
        "complaints": complaint_list
    })


def add_complaint(request):
    if not request.session.get("resident_id"):
        return redirect('resident_login')   
    resident_id=request.session.get("resident_id")
    resident=Resident.objects.get(id=resident_id)

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
    if not request.session.get("admin_logged_in"):
        return redirect("admin_login")

    total_residents = Resident.objects.count()
    total_apartments = Apartment.objects.count()
    total_complaints = Complaint.objects.count()
    total_payments = Payment.objects.count()

    maintenance_members = MaintenanceTeam.objects.all()

    return render(
        request,
        "core/admin_dashboard.html",
        {
            "total_residents": total_residents,
            "total_apartments": total_apartments,
            "total_complaints": total_complaints,
            "total_payments": total_payments,
            "maintenance_members": maintenance_members,
        }
    )


def manage_residents(request):
    if not request.session.get("admin_logged_in"):
        return redirect('admin_login')

    apartments = Apartment.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        apartment_id = request.POST.get("apartment")

        apartment = Apartment.objects.get(id=apartment_id)

        Resident.objects.create(
            name=name,
            email=email,
            phone=phone,
            apartment=apartment
        )

        return redirect('manage_residents')

    residents = Resident.objects.all()

    return render(request, 'core/manage_residents.html', {
        'residents': residents,
        'apartments': apartments
    })

def manage_apartments(request):
    if not request.session.get("admin_logged_in"):
        return redirect('admin_login')

    if request.method == "POST":
        apartment_number = request.POST.get("apartment_number")
        floor = request.POST.get("floor")
        block = request.POST.get("block")

        Apartment.objects.create(
            apartment_number=apartment_number,
            floor=floor,
            block=block
        )

        return redirect('manage_apartments')

    apartments = Apartment.objects.all()

    return render(request, 'core/manage_apartments.html', {
        'apartments': apartments
    })

from decimal import Decimal

def admin_payments(request):
    if not request.session.get("admin_logged_in"):
        return redirect("admin_login")

    residents = Resident.objects.all()
    payments = Payment.objects.all()

    if request.method == "POST":

        action = request.POST.get("action")
        resident_id = request.POST.get("resident")

        resident = Resident.objects.get(id=resident_id)

        # Change Total Amount
        if action == "update_total":
            new_total = request.POST.get("total_amount")

            if new_total:
                resident.total_amount = Decimal(new_total)
                resident.save()

            return redirect("admin_payments")

        # Add Payment
        if action == "add_payment":
            amount = request.POST.get("amount")

            if amount:
                Payment.objects.create(
                    resident=resident,
                    amount=Decimal(amount),
                    status="PAID"
                )

            return redirect("admin_payments")

    # Overall amounts
    total_amount = sum(
        (resident.total_amount for resident in residents),
        Decimal("0")
    )

    paid_amount = sum(
        (
            payment.amount
            for payment in payments
            if payment.status == "PAID"
        ),
        Decimal("0")
    )

    pending_amount = total_amount - paid_amount

    # Resident-wise payment details
    payment_list = []

    for resident in residents:

        resident_payments = payments.filter(
            resident=resident
        )

        paid = sum(
            (
                payment.amount
                for payment in resident_payments
                if payment.status == "PAID"
            ),
            Decimal("0")
        )

        pending = resident.total_amount - paid

        # Avoid negative pending
        if pending < 0:
            pending = Decimal("0")

        latest_payment = resident_payments.filter(
            status="PAID"
        ).order_by("-payment_date").first()

        payment_list.append({
            "id": resident.id,
            "name": resident.name,
            "total": resident.total_amount,
            "paid": paid,
            "pending": pending,
            "status": "Paid" if paid > 0 else "Pending",
            "date": latest_payment.payment_date
                    if latest_payment else "—"
        })

    return render(
        request,
        "core/admin_payments.html",
        {
            "residents": residents,
            "total_amount": total_amount,
            "paid_amount": paid_amount,
            "pending_amount": pending_amount,
            "payment_list": payment_list
        }
    )
def admin_complaints(request):
    complaints=Complaint.objects.all()
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
        return redirect("admin_login")

    members = MaintenanceTeam.objects.all()

    return render(
        request,
        "core/admin_maintenance.html",
        {
            "members": members
        }
    )


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

def maintenance(request):
    teams = MaintenanceTeam.objects.all()

    return render(
        request,
        'core/maintenance.html',
        {'teams': teams}
    )

def delete_resident(request, resident_id):
    if not request.session.get("admin_logged_in"):
        return redirect("admin_login")

    if request.method == "POST":
        resident = get_object_or_404(Resident, id=resident_id)
        resident.delete()

    return redirect("manage_residents")


def otp_verification(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '').strip()
        session_otp = str(request.session.get('otp', ''))
        email = request.session.get('email')

        if not session_otp or not email:
            messages.error(request, "OTP expired. Please sign in again.")
            return redirect('sign_in')

        if entered_otp == session_otp:
            try:
                resident = Resident.objects.get(email=email)

                request.session['resident_id'] = resident.id
                request.session.pop('otp', None)
                request.session.pop('email', None)

                return redirect('resident_dashboard')

            except Resident.DoesNotExist:
                messages.error(request, "Resident email not found.")
                return redirect('sign_in')

        else:
            messages.error(request, "Incorrect OTP. Please try again.")

    return render(request, 'core/otp_verification.html')
def maintenance_logout(request):
    request.session.pop('maintenance_member_id',None)
    return redirect('maintenance_login')
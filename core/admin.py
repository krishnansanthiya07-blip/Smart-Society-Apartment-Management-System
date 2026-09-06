from django.contrib import admin
from .models import Resident,Apartment,Payment,Complaint,MaintenanceTeam

# Register your models here.
admin.site.register(Resident)
admin.site.register(Apartment)
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('resident', 'amount', 'payment_date', 'status')
admin.site.register(Complaint)
admin.site.register(MaintenanceTeam)
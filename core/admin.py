from django.contrib import admin

from .models import (
    Resident,
    Apartment,
    Resident,
    Payment,
    Complaint,
    MaintenanceTeam
)

admin.site.register(Apartment)
admin.site.register(Resident)
admin.site.register(Payment)
admin.site.register(Complaint)
admin.site.register(MaintenanceTeam)
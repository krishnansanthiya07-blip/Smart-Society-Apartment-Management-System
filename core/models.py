from django.db import models


class Apartment(models.Model):
    apartment_number = models.CharField(max_length=20, unique=True)
    floor = models.IntegerField()
    block = models.CharField(max_length=20)

    def __str__(self):
        return self.apartment_number


class Resident(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    apartment = models.OneToOneField(
        Apartment,
        on_delete=models.CASCADE
    )
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    resident = models.ForeignKey(
        Resident,
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("PAID", "Paid"),
            ("PENDING", "Pending"),
        ],
        default="PENDING"
    )

    def __str__(self):
        return f"{self.resident.name} - {self.amount}"


class Complaint(models.Model):
    resident = models.ForeignKey(
        Resident,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("PENDING", "Pending"),
            ("IN_PROGRESS", "In Progress"),
            ("RESOLVED", "Resolved"),
        ],
        default="PENDING"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class MaintenanceTeam(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name
from django.contrib.auth.models import User
from django.db import models


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patient_id = models.CharField(max_length=10, unique=True)
    date_of_birth = models.DateField()
    blood_type = models.CharField(max_length=5)
    allergies = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.patient_id})"


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"Dr. {self.user.last_name} ({self.speciality})"


class MedicalRecord(models.Model):
    RECORD_TYPES = [
        ("DIAGNOSIS", "Diagnosis"),
        ("PRESCRIPTION", "Prescription"),
        ("LAB", "Lab Result"),
        ("IMAGING", "Imaging"),
    ]

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="records"
    )
    record_type = models.CharField(max_length=20, choices=RECORD_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    doctor_name = models.CharField(max_length=100)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.record_type}: {self.title} for {self.patient.patient_id}"


class Appointment(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="appointments"
    )
    doctor_name = models.CharField(max_length=100)
    appointment_date = models.DateTimeField()
    reason = models.TextField()

    def __str__(self):
        return f"Appointment with {self.doctor_name} on {self.appointment_date}"


class Prescription(models.Model):
    record = models.OneToOneField(
        MedicalRecord, on_delete=models.CASCADE, related_name="prescription"
    )
    medication_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)

    def __str__(self):
        return (
            f"Prescription: {self.medication_name} for {self.record.patient.patient_id}"
        )

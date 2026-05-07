import os
import sys
from datetime import date, datetime

import django

# Add the project root to sys.path
sys.path.append(os.path.join(os.getcwd(), "src"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.settings")
django.setup()

from django.contrib.auth.models import User

from src.pages.models import Appointment, Doctor, MedicalRecord, Patient


def populate():
    print("Populating database...")

    # Create Users
    u1, _ = User.objects.get_or_create(
        username="john_doe", first_name="John", last_name="Doe"
    )
    u1.set_password("test1234")
    u1.save()

    u2, _ = User.objects.get_or_create(
        username="jane_smith", first_name="Jane", last_name="Smith"
    )
    u2.set_password("test1234")
    u2.save()

    u3, _ = User.objects.get_or_create(
        username="bob_wilson", first_name="Bob", last_name="Wilson"
    )
    u3.set_password("test1234")
    u3.save()

    # Create Doctor User
    ud, _ = User.objects.get_or_create(
        username="dr_house", first_name="Gregory", last_name="House"
    )
    ud.set_password("test1234")
    ud.save()

    # Create Patients
    p1, _ = Patient.objects.get_or_create(
        user=u1,
        defaults={
            "patient_id": "PAT000001",
            "date_of_birth": date(1985, 5, 12),
            "blood_type": "O+",
            "allergies": "Peanuts",
        },
    )
    p2, _ = Patient.objects.get_or_create(
        user=u2,
        defaults={
            "patient_id": "PAT000002",
            "date_of_birth": date(1992, 8, 24),
            "blood_type": "A-",
            "allergies": "Penicillin",
        },
    )
    p3, _ = Patient.objects.get_or_create(
        user=u3,
        defaults={
            "patient_id": "PAT000003",
            "date_of_birth": date(1978, 11, 3),
            "blood_type": "B+",
            "allergies": "None",
        },
    )

    # Create Doctor profile
    Doctor.objects.get_or_create(
        user=ud, defaults={"specialty": "Diagnostics", "employee_id": "DOC001"}
    )

    # Create Medical Records
    MedicalRecord.objects.get_or_create(
        patient=p1,
        record_type="DIAGNOSIS",
        title="Seasonal Allergies",
        description="Patient reports sneezing and itchy eyes during spring.",
        doctor_name="Dr. House",
        notes="Advised taking antihistamines.",
    )

    MedicalRecord.objects.get_or_create(
        patient=p1,
        record_type="PRESCRIPTION",
        title="Loratadine 10mg",
        description="Take one tablet daily as needed for allergy symptoms.",
        doctor_name="Dr. House",
        notes="Patient should avoid peanut products as previously noted.",
    )

    MedicalRecord.objects.get_or_create(
        patient=p2,
        record_type="LAB",
        title="Blood Panel",
        description="Routine annual blood work. All levels within normal range.",
        doctor_name="Dr. Grey",
        notes="No action required.",
    )

    # Create Appointments
    Appointment.objects.get_or_create(
        patient=p1,
        doctor_name="Dr. House",
        appointment_date=datetime(2026, 6, 15, 10, 30),
        reason="Follow-up on allergy treatment",
    )

    Appointment.objects.get_or_create(
        patient=p2,
        doctor_name="Dr. Grey",
        appointment_date=datetime(2026, 7, 2, 14, 0),
        reason="Annual physical examination",
    )

    print("Database populated successfully!")


if __name__ == "__main__":
    populate()

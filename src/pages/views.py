from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt

from .models import Appointment, MedicalRecord, Patient


def home(request):
    return render(request, "home.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        dob = request.POST.get("dob")

        patient_id = f"PAT{str(Patient.objects.count() + 1).zfill(6)}"

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        Patient.objects.create(
            user=user,
            patient_id=patient_id,
            date_of_birth=dob,
            blood_type="Unknown",
            allergies="None",
        )

        login(request, user)
        return redirect("dashboard")
    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def dashboard(request):
    patient = None
    try:
        patient = Patient.objects.get(user=request.user)
        records = MedicalRecord.objects.filter(patient=patient).order_by(
            "-date_created"
        )
        appointments = Appointment.objects.filter(patient=patient).order_by(
            "appointment_date"
        )
    except Patient.DoesNotExist:
        records = []
        appointments = []
    is_doctor = hasattr(request.user, "doctor")
    return render(
        request,
        "dashboard.html",
        {
            "patient": patient,
            "records": records,
            "appointments": appointments,
            "is_doctor": is_doctor,
        },
    )


@login_required
def search_records(request):
    query = request.GET.get("q", "")
    records = []
    if query:
        try:
            patient = Patient.objects.get(user=request.user)
            patient_clause = f"patient_id = {patient.id} AND "
        except Patient.DoesNotExist:
            return render(request, "error.html")

        cursor = connection.cursor()
        # Flaw nº1 : SQL Injection
        # Fix : Use parametrized query
        # cursor.execute(
        #     f"SELECT id, title, description FROM pages_medicalrecord WHERE {patient_clause}title LIKE %s",
        #     [f"%{query}%"],
        # )
        cursor.execute(
            f"SELECT id, title, description FROM pages_medicalrecord WHERE {patient_clause}title LIKE '%{query}%'"
        )
        records = cursor.fetchall()

    return render(request, "search_records.html", {"records": records, "query": query})


@login_required
def add_note(request):
    if request.method == "POST":
        record_id = request.POST.get("record_id")
        note_text = request.POST.get("note")

        if not record_id:
            return redirect("dashboard")

        record = get_object_or_404(MedicalRecord, id=record_id)

        # Flaw nº2 : XSS Injection
        # Fix : Sanitize the text
        # record.notes = escape(note_text)
        record.notes = note_text
        record.save()

        return redirect("dashboard")

    record_id = request.GET.get("record_id")
    return render(request, "add_note.html", {"record_id": record_id})


@login_required
def view_patient_data(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)
    # Flaw nº3 : IDOR
    # Fix : Check if the patient belongs to the current user
    # if patient.user != request.user:
    #     return render(request, 'error.html')
    records = MedicalRecord.objects.filter(patient=patient)
    return render(
        request,
        "patient_data.html",
        {
            "patient": patient,
            "records": records,
        },
    )


@login_required
def api_get_record(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id)
    # Flaw nº3 : IDOR
    # Fix : Check if the record belongs to the current user
    # if record.patient.user != request.user:
    #     return JsonResponse({ 'error': 'Unauthorized' }, status=403)
    return JsonResponse(
        {
            "id": record.id,
            "patient_id": record.patient.id,
            "title": record.title,
            "description": record.description,
            "notes": record.notes,
        }
    )


@login_required
def export_data(request):  # TODO Flaw nº4 : No encryption
    pass


# Flaw nº5 : CSRF
# Fix : Remove decorator @csrf_exempt
@csrf_exempt
@login_required
def update_patient_info(request):
    if request.method == "POST":
        patient = get_object_or_404(Patient, user=request.user)
        patient.allergies = request.POST.get("allergies", patient.allergies)
        patient.blood_type = request.POST.get("blood_type")
        patient.save()
        return redirect("dashboard")
    return redirect("dashboard")

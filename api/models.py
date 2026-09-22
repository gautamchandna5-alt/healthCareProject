from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"

class Patient(models.Model):
    # Tracks which authenticated user created this patient record
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients')
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PatientDoctorMapping(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='doctor_mappings')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patient_mappings')
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevents assigning the same doctor to a patient multiple times
        unique_together = ('patient', 'doctor')

    def __str__(self):
        return f"{self.patient.name} -> {self.doctor.name}"
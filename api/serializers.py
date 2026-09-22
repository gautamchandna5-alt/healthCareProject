from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Doctor, Patient, PatientDoctorMapping

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name')
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', '')
        )
        return user

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    # Make user read-only so it can be populated automatically via the View
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Patient
        fields = '__all__'

class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    doctor_details = DoctorSerializer(source='doctor', read_only=True)
    patient_details = PatientSerializer(source='patient', read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ('id', 'patient', 'doctor', 'assigned_at', 'doctor_details', 'patient_details')
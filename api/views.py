from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Doctor, Patient, PatientDoctorMapping
from .serializers import (
    RegisterSerializer, DoctorSerializer, 
    PatientSerializer, PatientDoctorMappingSerializer
)

# --- 1. Authentication APIs ---

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

# --- 2. Patient Management APIs ---

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only view and manage patients they created
        return Patient.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as the creator
        serializer.save(user=self.request.user)

# --- 3. Doctor Management APIs ---

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

# --- 4. Patient-Doctor Mapping APIs ---

class MappingListCreateView(generics.ListCreateAPIView):
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Validate that the patient belongs to the authenticated user
        patient_id = request.data.get('patient')
        if not Patient.objects.filter(id=patient_id, user=request.user).exists():
            return Response(
                {"error": "Patient does not exist or you do not have permission."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

class MappingDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # GET /api/mappings// - Retrieves doctors for a specific patient
        # Validates that the patient belongs to the requesting user
        if not Patient.objects.filter(id=pk, user=request.user).exists():
            return Response({"error": "Not found or unauthorized."}, status=status.HTTP_404_NOT_FOUND)
            
        mappings = PatientDoctorMapping.objects.filter(patient_id=pk)
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        # DELETE /api/mappings// - Deletes a specific mapping record
        try:
            mapping = PatientDoctorMapping.objects.get(id=pk)
            # Ensure the user owns the patient in this mapping
            if mapping.patient.user != request.user:
                return Response({"error": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)
            
            mapping.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PatientDoctorMapping.DoesNotExist:
            return Response({"error": "Mapping not found."}, status=status.HTTP_404_NOT_FOUND)
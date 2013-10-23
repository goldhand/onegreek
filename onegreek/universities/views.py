from rest_framework import viewsets

from .serializers import UniversitySerializer
from .models import University

class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

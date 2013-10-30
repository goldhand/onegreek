from rest_framework import viewsets

from .models import Fraternity
from .serializers import FraternitySerializer

class FraternityViewSet(viewsets.ModelViewSet):
    queryset = Fraternity.objects.all()
    serializer_class = FraternitySerializer

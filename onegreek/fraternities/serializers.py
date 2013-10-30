from rest_framework import serializers

from .models import Fraternity


class FraternitySerializer(serializers.HyperlinkedModelSerializer):
    description = serializers.WritableField(source='description')

    class Meta:
        model = Fraternity
        fields = ['url', 'title', 'description', 'gpa', 'group']

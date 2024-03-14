from rest_framework import serializers

from core.models import ImportanceLevel, Color


class ImportanceLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportanceLevel
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


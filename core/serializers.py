from rest_framework import serializers

from core.models import ImportanceLevel


class ImportanceLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportanceLevel
        fields = '__all__'

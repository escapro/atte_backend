from rest_framework import serializers
from .models import *


class ShiftSerializer(serializers.ModelSerializer):
    shift_type = serializers.CharField(source='get_shift_type_display')

    class Meta:
        model = Shift
        fields = '__all__'

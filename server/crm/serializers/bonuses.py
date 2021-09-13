from rest_framework import serializers
from crm.models import Bonuses


class BonuseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bonuses
        fields = '__all__'

class BonuseCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bonuses
        fields = ('revenue_to', 'rate')
        extra_kwargs = {
            'revenue_to': {'required': True},
            'rate': {'required': True},
        }


from rest_framework.serializers import ModelSerializer
from funnels.models import Funnel, Funnel_message

class FunnelSerializer(ModelSerializer):
    class Meta:
        model = Funnel
        fields = '__all__'


class FunnelMessageSerializer(ModelSerializer):
    class Meta:
        model = Funnel_message
        fields = '__all__'
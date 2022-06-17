from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from trading.models import Bundle, BinanceBudle, BinancePair
import datetime
from django.utils import timezone

class BundleSerializer(ModelSerializer):
    time_ago = serializers.SerializerMethodField('get_time_ago')

    def get_time_ago(self, bundle_object):

        data = timezone.now() - bundle_object.date
        return round(data.total_seconds())


    class Meta:
        model = Bundle
        fields = ['start_symbol', 'one_step','two_step', 'final_step','profitability','time_ago']

class BinancePairSerializer(ModelSerializer):
    class Meta:
        model = BinancePair
        fields = "__all__"

class BinancePairRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            'name': value.symbol,
            'id':value.pk
        }

class BinanceBundleSerializer(ModelSerializer):
    first_pair = BinancePairRelatedField(read_only=True,many=False)
    second_pair = BinancePairRelatedField(read_only=True,many=False)
    third_pair = BinancePairRelatedField(read_only=True,many=False)

    class Meta:
        model = BinanceBudle
        fields = ['start_stop_symbol', 'first_pair','second_pair', 'third_pair']
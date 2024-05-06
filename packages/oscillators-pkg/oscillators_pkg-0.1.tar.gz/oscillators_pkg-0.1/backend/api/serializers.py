# serializers.py
from rest_framework import serializers

class OscillatorsSerializer(serializers.Serializer):
    k1 = serializers.FloatField()
    r1 = serializers.FloatField()
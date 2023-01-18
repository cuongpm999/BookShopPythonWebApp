from rest_framework import serializers

class ApiSerializer(serializers.Serializer):
    idShipment = serializers.IntegerField(default=0)
    priceShipment = serializers.FloatField(default=0)

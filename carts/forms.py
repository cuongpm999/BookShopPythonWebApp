from rest_framework import serializers

class ApiSerializer(serializers.Serializer):
    barCode = serializers.CharField(max_length=255)
    totalQuantity = serializers.IntegerField(default=0)
    quantity = serializers.IntegerField(default=0)
    price = serializers.FloatField(default=0)
    totalAmount = serializers.FloatField(default=0)
    
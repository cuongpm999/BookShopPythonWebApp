import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from orders.forms import ApiSerializer
from orders.models import  Shipment

# Create your views here.
class SelectShipment(APIView):
    def post(self, request, format=None):
        serializer = ApiSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            idShipment_ = json.loads(json.dumps(serializer.data))['idShipment']
            shipment = Shipment.objects.get(id=idShipment_)
            serializer = ApiSerializer({'priceShipment': shipment.price})
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
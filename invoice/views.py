from django.shortcuts import HttpResponse
from rest_framework import generics
from rest_framework.views import APIView
from uuid import uuid4
from .serializers import (ProductSerializer,InvoiceSerializer)
from .models import (Product, Invoice, InvoiceProduct)
from invoice import serializers


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

class InvoiceCreate(APIView):
    """ 
    """
    def post(self, request, format=None):
        serializer = InvoiceSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            print("valid serializer")
            print(serializer.validated_data.get('customer').get('username'))
        else:
            print("invalid serialzier")
        
        return HttpResponse('<h1>Done</h1>')
        

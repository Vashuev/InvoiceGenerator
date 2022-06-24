from django.shortcuts import HttpResponse
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (ProductSerializer,InvoiceSerializer)
from .models import (Product, Invoice)

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

class InvoiceAPIView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(context={'request':request},data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'error' : 'Transactional Error'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})

class InvoiceUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    lookup_field = 'slug'

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_queryset().get(slug=request.data['slug'])
        except:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, 
                data={'meassage': 'no invoice found in database with slug = {}'.format(request.data['slug'])}
            )
        serializer = self.get_serializer_class()(instance,request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'error' : 'Transactional Error'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})

from asyncio.windows_events import NULL
from functools import partial
from logging import NullHandler
from rest_framework import serializers
from .models import Product, Invoice, InvoiceProduct
from django.db import transaction
from rest_framework.serializers import ValidationError
from .serializerFunctions import (
    CreateInvoice, AddProducts, UpdateProducts
)
from .validatorFunctions import (
    ValidateStockQuantityPost, ValidateStockQuantityPut,
    ValidatePhoneNumber
)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        lookup_field = 'slug'

class InvoiceProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceProduct
        fields = '__all__'
        extra_kwargs = {'invoiceId': {'required': False}} 

class InvoiceSerializer(serializers.ModelSerializer):
    products = InvoiceProductSerializer(many=True)
    class Meta:
        model = Invoice
        fields = ['id', 'number', 'status','dueDate',
        'customerName', 'phoneNumber', 'slug', 'products']
        lookup_field = 'slug'
        extra_kwargs = {'number': {'required': False}} 

    def validate(self, data):
        # validating products quantity 
        print("data = ", data)
        if self.context['request'].method == 'POST':
            ValidatePhoneNumber(data.get('phoneNumber'))
            ValidateStockQuantityPost(data.get('products'))
            print("Check Post")
        elif (self.context['request'].method == 'PUT' or self.context['request'].method == 'PATCH'):
            if data.get('phoneNumber'):
                ValidatePhoneNumber(data.get('phoneNumber'))
            if data.get('slug'):
                ValidateStockQuantityPut(data.get('products'), data.get('slug'))
            else:
                raise ValidationError({'slug' : 'Invoice slug is Required field for update'})
        return data

    def create(self, validated_data):
        with transaction.atomic():
            instance = CreateInvoice(validated_data)
            AddProducts(validated_data.get('products'), instance)
        return instance

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.status = validated_data.get('status', instance.status)
            instance.dueDate = validated_data.get('dueDate', instance.dueDate)
            instance.customerName = validated_data.get('customerName', instance.customerName)
            instance.phoneNumber = validated_data.get('phoneNumber', instance.phoneNumber)
            instance.save()
            UpdateProducts(validated_data.get('products'), instance)
        return instance
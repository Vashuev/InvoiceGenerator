from rest_framework import serializers
from .models import Product, Invoice, InvoiceProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        lookup_field = 'slug'

class InvoiceProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceProduct
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    products = InvoiceProductSerializer(many=True, partial=True)
    
    class Meta:
        model = Invoice
        fields = ['id', 'number','status', 'dueDate', 'customer', 'products','slug']
        lookup_field = 'slug'
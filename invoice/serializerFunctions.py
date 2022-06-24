from uuid import uuid4
from .models import Invoice, InvoiceProduct, Product
from rest_framework.serializers import ValidationError

def CreateInvoice(validatedData):
    """
        Creating a new Instance of Invoice 
        before adding products to it

    """
    instanceNumber = 'INV-'+str(uuid4()).split('-')[1]
    instanceStatus = validatedData.get('status')
    instanceCustomer = validatedData.get('customerName')
    instancePhoneNumber = validatedData.get('phoneNumber')

    return Invoice.objects.create(
        number = instanceNumber,
        status = instanceStatus,
        customerName = instanceCustomer,
        phoneNumber = instancePhoneNumber
    )

def AddProducts(products, invoiceInstance):
    """
        Adds new products and corrosponding quantity 
    """
    for product in products:
        productFromDb = Product.objects.get(id=product.get('productId').id)
        # adding products and quantity 
        InvoiceProduct.objects.create(invoiceId = invoiceInstance,
            productId = productFromDb,
            quantity = product.get('quantity')
        )

        # updating product's stock
        productFromDb.stock -= product.get('quantity')
        productFromDb.save()

def UpdateProducts(products, invoiceInstance):
    """
        Removes earlier products, and it's quantity
        adds new products and quantity
    """
    for instance in InvoiceProduct.objects.filter(invoiceId=invoiceInstance):
        instance.productId.stock += instance.quantity
        instance.productId.save()
        instance.delete()
    AddProducts(products, invoiceInstance)



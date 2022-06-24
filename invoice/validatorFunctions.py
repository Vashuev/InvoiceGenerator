from .models import Invoice, InvoiceProduct, Product
from rest_framework.serializers import ValidationError

def ValidateStockQuantityPost(products):
    """
        checking every product's stock, and raising exception at the end if any
    """
    errors = {}
    for product in products:
        productInstance = product.get('productId')
        if productInstance.stock < product.get('quantity'):
            errors['product - {}, id - {}'.format(productInstance.name, productInstance.id)] = 'quantity must be less or equal to {}'.format(productInstance.stock)

    if errors:
        raise ValidationError(errors)
    
def ValidateStockQuantityPut(products, slug):
    """
        Validate wheater update quantity is available in the stock
    """
    InvoiceProducts = InvoiceProduct.objects.filter(invoiceId=Invoice.objects.get(slug=slug))
    earlierProducts = [instance.productId for instance in InvoiceProducts]
    errors = {}
    for product in products:
        productInstance = product.get('productId')
        if productInstance in earlierProducts:
            earlierProduct = InvoiceProducts.get(productId = productInstance)
            if (productInstance.stock +  earlierProduct.quantity < product.get('quantity')):
                errors['product - {}, id - {}'.format(productInstance.name, productInstance.id)] = 'quantity must be less or equal to {}'.format(productInstance.stock + earlierProduct.quantity)
        elif productInstance.stock < product.get('quantity'):
            errors['product - {}, id - {}'.format(productInstance.name, productInstance.id)] = 'quantity must be less or equal to {}'.format(productInstance.stock)
    if errors:
        raise ValidationError(errors)


def ValidatePhoneNumber(phoneNumber):
    """
        Validating Phone Number
    """
    errors = {}
    if phoneNumber.isnumeric() == False:
        errors['phoneNumber (integer)'] = 'should be integer 0-9'
    if len(phoneNumber) != 10:
        errors['phoneNumber (lenght)'] = 'lenght must be equal to 10'
    if errors:
        raise ValidationError(errors)
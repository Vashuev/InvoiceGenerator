from .models import InvoiceProduct


def get_context(instance):
    # context with Customer Details
    context = {
        'number' : instance.number, 
        'customerName' : instance.customerName,
        'phoneNumber' : instance.phoneNumber,
        'customerAddress' : instance.customerAddress,
        'status' : instance.status,
    }

    # adding products details
    products = []
    total_quantity = 0
    total_price = 0.0
    for invoiceInstance in InvoiceProduct.objects.filter(invoiceId=instance):
        products.append({
            'name' : invoiceInstance.productId.name,
            'description': invoiceInstance.productId.description,
            'pricePerUnit' : invoiceInstance.productId.price,
            'quantity' : invoiceInstance.quantity,
            'price' : float(invoiceInstance.productId.price) * float(invoiceInstance.quantity)
        })
        total_quantity += invoiceInstance.quantity
        total_price += float(invoiceInstance.productId.price) * float(invoiceInstance.quantity)

    context['products'] = products
    context['total_quantity'] = total_quantity
    context['total_price'] = total_price

    return context
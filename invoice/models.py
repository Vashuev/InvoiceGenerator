from django.template.defaultfilters import slugify
from uuid import uuid4
from django.db import models
from django.urls import reverse      

class Product(models.Model):
    """
        TABLE: Product
        COLUMNS : ( name | description | price | stock | metric )
        DESCRIPTION : stores various Products, stock, and metric to measure them
    """
    METRIC_CHOICE = (
        ('KILOGRAM', 'KILOGRAM'),
        ('LITER', 'LITER'),
        ('PACKET', 'PACKET'),
        ('PIECE', 'PIECE')
    )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    metric = models.CharField(choices=METRIC_CHOICE, max_length=10)

    # utilities fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
        
        self.slug = slugify('{} {}'.format(self.name, self.uniqueId))
        super(Product, self).save(*args, **kwargs)
    

class Invoice(models.Model):
    """
        TABLE: Invoice
        COLUMNS : ( number | status | dueDate | customerName | phoneNumber )
        DESCRIPTION : store invoice associated with a Customer
    """
    INVOICE_STATUS = (
        ('DRAFT', 'DRAFT'),
        ('ISSUED', 'ISSUED'),
        ('PAID', 'PAID'),
    )

    # Invoice related fields
    number = models.CharField(max_length=12)
    status = models.CharField(choices=INVOICE_STATUS, max_length=10)
    dueDate = models.DateField(auto_now=True)

    # Customer related Fields
    customerName = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=12)
    
    # utilities fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)

    def __str__(self) -> str:
        return self.number

    def get_absolute_url(self):
        return reverse('invoice-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
        
        self.slug = slugify('{} {}'.format(self.number, self.uniqueId))
        super(Invoice, self).save(*args, **kwargs)


class InvoiceProduct(models.Model):
    """
        TABLE : Product
        COLUMNS : ( invoiceId, productId, quantity )
        DESCRIPTION : keep track of Products and their quantity asked by the
            customer, it links those products with corrosponding invoice

    """
    invoiceId = models.ForeignKey(to=Invoice, related_name='products', on_delete=models.CASCADE)
    productId = models.ForeignKey(to=Product, related_name='invoice',on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.invoiceId.number + self.productId.name
    


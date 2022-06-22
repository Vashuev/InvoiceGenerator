from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.ProductList.as_view(), name='product_list'),
    path('product/detail/<slug:slug>/', views.ProductDetail.as_view(), name='product_detail'),
    path('invoice/', views.InvoiceCreate.as_view(), name='invoice_create'),
]

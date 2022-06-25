from django.urls import path
from . import views
from django.views.generic import TemplateView
urlpatterns = [
    path('product/', views.ProductList.as_view(), name='product_list'),
    path('product/<slug:slug>/', views.ProductDetail.as_view(), name='product_detail'),
    path('invoice/', views.InvoiceAPIView.as_view(), name='invoice_create'),
    path('invoice/<slug:slug>/', views.InvoiceUpdateView.as_view(), name='invoice_update'),
    path('render_pdf_view/<slug:slug>/', views.render_pdf_view, name='invoice_pdf'),
]

from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (ProductSerializer,InvoiceSerializer)
from .models import (Product, Invoice, InvoiceProduct)

from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import UserSerializer

class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

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
            instance = self.get_queryset().get(slug=kwargs['slug'])
        except:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, 
                data={'meassage': 'no invoice found in database with slug value = {}'.format(kwargs['slug'])}
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

## PDF geneator view ###

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from rest_framework.decorators import api_view
from .viewFunctions import get_context

@api_view(['GET'])
def render_pdf_view(request, *args, **kwargs):

    try:
        instance = Invoice.objects.get(slug=kwargs['slug'])
    except:
        return Response(
            status=status.HTTP_400_BAD_REQUEST, 
            data={'meassage': 'no invoice found in database with slug value = {}'.format(kwargs['slug'])}
        )
    context = get_context(instance)
    print("context", context)
    template_path = 'invoice.html'
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    filename = "invoice{}.pdf".format(context['number'])
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


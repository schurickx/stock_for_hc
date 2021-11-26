from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Provider, Position, Category, Entity, Invoice
from .serializers import PositionSerializer, ProviderSerializer, CategorySerializer, EntitySerializer, InvoiceSerializer
from rest_framework.authentication import BasicAuthentication

from .utils import CsrfExemptSessionAuthentication


def index(request):
    return HttpResponse("Home")


class PositionViewSet(ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('id', 'provider', 'category',)
    ordering_fields = '__all__'


class ProviderViewSet(ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Provider.objects.all().order_by('title')
    serializer_class = ProviderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('id', 'title')
    ordering_fields = ('title',)


class CategoryViewSet(ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('id', 'title')
    ordering_fields = ('title',)


class EntityViewSet(ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('id', 'title')
    ordering_fields = ('title',)


class InvoiceViewSet(ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('id', 'title', 'provider', 'shipping_date',)
    ordering_fields = ('title', 'shipping_date')

from django.db.models import Sum, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import BasicAuthentication
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Provider, Position, Category, Entity, Invoice, Operation, OperationDetail, Stock
from .serializers import PositionSerializer, ProviderSerializer, CategorySerializer, EntitySerializer, \
    InvoiceSerializer, OperationSerializer, OperationDetailSerializer, StockSerializer
from .utils import CsrfExemptSessionAuthentication


class PositionViewSet(ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ('id', 'provider', 'category',)
    ordering_fields = '__all__'


class ProviderViewSet(ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Provider.objects.all().order_by('title')
    serializer_class = ProviderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ('id', 'title')
    ordering_fields = ('title',)


class CategoryViewSet(ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ('id', 'title')
    ordering_fields = ('title',)


class EntityViewSet(ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ('id', 'title')
    ordering_fields = ('title',)


class InvoiceViewSet(ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ('id', 'title', 'provider', 'shipping_date',)
    ordering_fields = ('title', 'shipping_date')


class OperationViewSet(ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ('id', 'kind', 'shipping_date')
    ordering_fields = ('shipping_date',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OperationDetailViewSet(ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = OperationDetail.objects.all().order_by('-pk')
    serializer_class = OperationDetailSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ('operation', 'stock',)
    ordering_fields = ('operation', 'stock',)


class StockViewSet(ReadOnlyModelViewSet):
    queryset = Stock.objects.all().annotate(
        quantity=Sum('operationdetail__quantity')).annotate(
        price_sum=F('price') * F('quantity'))
    # queryset = Stock.objects.all()
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ('entity', 'position', 'invoice', 'price',)
    ordering_fields = ('position', 'time_create', 'entity', 'price',)

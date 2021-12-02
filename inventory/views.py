from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, get_object_or_404
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
    queryset = OperationDetail.objects.all()
    serializer_class = OperationDetailSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ('operation', 'position',)
    ordering_fields = ('operation',)

    def update_stock(self, serializer):
        data = serializer.validated_data
        params = {
            'position': data.get('position'),
            'entity': data.get('entity'),
            'invoice': data.get('invoice'),
            'price': data.get('price'),
        }
        quantity = data.get('quantity')
        type_operation = data.get('operation').kind

        try:
            instance = Stock.objects.get(**params)
            if type_operation == 'IN':
                instance.quantity += quantity
            if type_operation == 'OUT':
                if instance.quantity < quantity:
                    raise ValidationError(
                        'Количество позиций для списания превышает наличие на складе')
                if instance.quantity == quantity:
                    return instance.delete()
                if instance.quantity > quantity:
                    instance.quantity -= quantity
            return instance.save()
        except Stock.DoesNotExist:
            if type_operation == 'IN':
                stock_serializer = StockSerializer(data=self.request.data)
                stock_serializer.is_valid(raise_exception=True)
                stock_serializer.save()
            if type_operation == 'OUT':
                raise ValidationError('Данной позиции нет в наличии на складе')

    def perform_create(self, serializer):
        self.update_stock(serializer)
        super().perform_create(serializer)

    def perform_update(self, serializer):
        # instance = self.get_object()
        # if serializer.validated_data.get('quantity') != instance.quantity:
        # self.update_stock(serializer)
        super().perform_update(serializer)


# class StockViewSet(ReadOnlyModelViewSet):
class StockViewSet(ReadOnlyModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ('entity', 'position', 'invoice',)
    ordering_fields = ('position', 'quantity', 'time_create',)

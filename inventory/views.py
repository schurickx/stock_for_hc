from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

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


class OperationViewSet(ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('id', 'kind', 'shipping_date')
    ordering_fields = ('shipping_date',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class OperationDetailViewSet(ModelViewSet):
#     authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
#     queryset = OperationDetail.objects.all()
#     serializer_class = OperationDetailSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [DjangoFilterBackend, OrderingFilter]
#     filterset_fields = ('operation', 'position',)
#     ordering_fields = ('operation',)

class OperationDetailViewSet(ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = OperationDetail.objects.all()
    serializer_class = OperationDetailSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('operation', 'position',)
    ordering_fields = ('operation',)

    def perform_create(self, serializer):
        data = serializer.validated_data
        position = data.get('position')
        entity = data.get('entity')
        invoice = data.get('invoice')
        price = data.get('price')
        quantity = data.get('quantity')
        type_operation = data.get('operation').kind
        instance = Stock.objects.filter(position=position, entity=entity,
                                        invoice=invoice, price=price)

        def is_exists(obj):
            if not obj.exists():
                raise ValidationError('Данной позиции нет в наличии на складе')
            return True

        def quantity_update(q_set, total):
            q_set.update(quantity=total)
            for q in q_set:
                q.save()

        if type_operation == 'IN':
            if instance.exists():
                quantity = instance[0].quantity + quantity
                quantity_update(instance, quantity)
            else:
                stock_serializer = StockSerializer(data=self.request.data)
                stock_serializer.is_valid(raise_exception=True)
                stock_serializer.save()
        if type_operation == 'OUT':
            if is_exists(instance) and instance[0].quantity > 0 and instance[0].quantity >= quantity:
                quantity = instance[0].quantity - quantity
                quantity_update(instance, quantity)
            else:
                raise ValidationError('Количество позиций для списания превышает наличие на складе')

        super().perform_create(serializer)


# class StockViewSet(ReadOnlyModelViewSet):
class StockViewSet(ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('entity', 'position', 'invoice',)
    ordering_fields = ('position', 'quantity', 'time_create',)

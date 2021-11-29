from rest_framework.serializers import ModelSerializer

from .models import Position, Provider, Category, Entity, OperationDetail, Invoice, Operation, Stock


class ProviderSerializer(ModelSerializer):
    class Meta:
        model = Provider
        fields = ('id', 'title')


class PositionSerializer(ModelSerializer):
    # provider = ProviderSerializer(read_only=True)

    class Meta:
        model = Position
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class EntitySerializer(ModelSerializer):
    class Meta:
        model = Entity
        fields = '__all__'


class InvoiceSerializer(ModelSerializer):
    class Meta:
        model = Invoice
        exclude = ('time_create', 'create_date',)
        # fields = '__all__'


class StockSerializer(ModelSerializer):
    class Meta:
        model = Stock
        # fields = '__all__'
        exclude = ('time_create', 'time_update',)


class OperationDetailSerializer(ModelSerializer):
    class Meta:
        model = OperationDetail
        fields = '__all__'


class OperationSerializer(ModelSerializer):
    class Meta:
        model = Operation
        fields = '__all__'

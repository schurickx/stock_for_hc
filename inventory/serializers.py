from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
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
    quantity = serializers.IntegerField(read_only=True)
    price_sum = serializers.DecimalField(read_only=True,
                                         max_digits=12, decimal_places=2)

    class Meta:
        model = Stock
        # fields = '__all__'
        exclude = ('time_create', 'time_update',)


class OperationDetailSerializer(ModelSerializer):
    new_stock_position = StockSerializer(
        many=False, required=False, allow_null=True, write_only=True)

    class Meta:
        model = OperationDetail
        fields = '__all__'
        extra_kwargs = {"stock": {'allow_null': True}, }

    def validate(self, data):
        stock = data.get('stock', None)
        new_stock_position = data.get('new_stock_position', None)
        if stock is None and new_stock_position is None:
            raise serializers.ValidationError(
                f"Поле stock и new_stock_position не могут быть одновременно пустыми")
        return data

    def create(self, validated_data):
        stock = validated_data.pop("stock", None)
        new_stock_position = validated_data.pop("new_stock_position", None)
        if stock is None and new_stock_position:
            stock, _ = Stock.objects.get_or_create(**new_stock_position)
        validated_data |= {"stock": stock}
        return super().create(validated_data)


class OperationSerializer(ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Operation
        fields = '__all__'

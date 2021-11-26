from rest_framework.serializers import ModelSerializer

from .models import Position, Provider, Category, Entity, OperationDetail, Invoice


class PositionSerializer(ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class ProviderSerializer(ModelSerializer):
    class Meta:
        model = Provider
        fields = ('id', 'title')


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class EntitySerializer(ModelSerializer):
    class Meta:
        model = Entity
        fields = '__all__'


class OperationDetailSerializer(ModelSerializer):
    class Meta:
        model = OperationDetail
        fields = '__all__'


class InvoiceSerializer(ModelSerializer):
    class Meta:
        model = Invoice
        exclude = ('time_create', 'create_date',)

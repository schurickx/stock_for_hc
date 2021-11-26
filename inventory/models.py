from datetime import date
from django.db import models


# Модель Перечень позиций
class Position(models.Model):
    THING = 'TH'
    KILOGRAM = 'KG'
    LITER = 'LT'
    UNIT = [(THING, 'шт.'), (KILOGRAM, 'кг.'), (LITER, 'л.'), ]

    title = models.CharField(max_length=255, verbose_name="Наименование")
    unit = models.CharField(max_length=2, choices=UNIT, default=THING, verbose_name="Единица измерения")
    provider = models.ForeignKey('Provider', on_delete=models.PROTECT, verbose_name="Поставщик")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, verbose_name="Категория позиции", null=True,
                                 blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'
        ordering = ['title', 'provider']


# Модель Поставщики
class Provider(models.Model):
    title = models.CharField(max_length=255, verbose_name="Поставщик")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
        ordering = ['title']


# Модель Категории
class Category(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name="Категория")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


# Модель Объекты
class Entity(models.Model):
    title = models.CharField(max_length=20, unique=True, verbose_name="Объекты")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'
        ordering = ['title']


# Модель Счетов
class Invoice(models.Model):
    title = models.CharField(max_length=100, verbose_name="Номер счёта")
    provider = models.ForeignKey('Provider', on_delete=models.SET_NULL, verbose_name="Поставщик", null=True)
    shipping_date = models.DateField(default=date.today, verbose_name="Дата отгрузки")
    create_date = models.DateField(default=date.today, verbose_name="Дата создания счета", blank=True, null=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Счёт'
        verbose_name_plural = 'Счета'
        ordering = ['shipping_date']


# Модель Полная позиция для склада
class AbstractFullPosition(models.Model):
    position = models.ForeignKey('Position', on_delete=models.PROTECT, verbose_name="Позиция", null=True)
    entity = models.ForeignKey('Entity', on_delete=models.PROTECT, verbose_name="Объект")
    invoice = models.ForeignKey('Invoice', on_delete=models.PROTECT, verbose_name="Счёт", null=True, blank=True)
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=11, decimal_places=2, verbose_name="Цена за единицу", blank=True)
    price_sum = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена общая", blank=True, editable=False)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")

    def __str__(self):
        return self.position

    def save(self, *args, **kwargs):
        self.price_sum = self.quantity * self.price
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


# Наличие склада
class Stock(AbstractFullPosition):

    def __str__(self):
        return str(self.position)

    class Meta:
        verbose_name = 'Наличие на складе'
        verbose_name_plural = 'Наличие на складе'


# Модель Операции
class Operation(models.Model):
    IN, OUT = 'IN', 'OUT'
    TYPE = (IN, "Приход"), (OUT, "Расход")
    kind = models.CharField(max_length=3, choices=TYPE, default=IN, verbose_name="Тип операции")
    shipping_date = models.DateField(default=date.today, verbose_name="Дата операции")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def __str__(self):
        return self.kind

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'


# Модель Позиции в операции
class OperationDetail(AbstractFullPosition):
    operation = models.ForeignKey('Operation', on_delete=models.CASCADE, verbose_name="Операция")
    position = models.ForeignKey('Position', on_delete=models.SET_NULL, verbose_name="Позиция", null=True)

    def __str__(self):
        return str(self.position)

    class Meta:
        verbose_name = 'Список операций по позициям'
        verbose_name_plural = 'Список операций по позициям'

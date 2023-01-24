from django.db import models
from autoslug import AutoSlugField
from django.urls import reverse
from datetime import date


class AssortmentCategory(models.Model):

    name = models.CharField(max_length=255, verbose_name="Имя категории")
    slug = AutoSlugField(populate_from='name', editable=True, always_update=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Location(models.Model):
    name = models.CharField(max_length=255, verbose_name="Локация")
    #slug = models.SlugField(unique=True)
    slug = AutoSlugField(populate_from='name', editable=True, always_update=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'


class AssortmentQualityCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя категории по качеству продукции")
    slug = AutoSlugField(populate_from='name', editable=True, always_update=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Quality of category'
        verbose_name_plural = 'Quality of categories'


class Product(models.Model):
    category = models.ForeignKey(AssortmentCategory, verbose_name="Категория", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, verbose_name="Название", null=False)
    description = models.TextField(max_length=2000, verbose_name="Описание", null=True, blank=True)
    slug = AutoSlugField(populate_from='name', editable=True, always_update=True)
    image = models.ImageField(verbose_name="Фотография", upload_to='photos_parts', default='default.jpg')
    comment = models.TextField(max_length=2000, verbose_name="Описание", null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/stock/{self.slug}'

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Product'


class Direction(models.Model):
    name = models.CharField(max_length=255, verbose_name="Куда/Откуда")

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=255, verbose_name="Куда/Откуда")

    def __str__(self):
        return self.name


class Transaction(models.Model):
    name = models.ForeignKey(Product, verbose_name="Название", on_delete=models.CASCADE, null=False)
    status = models.ForeignKey(Status, verbose_name="Статус", on_delete=models.CASCADE, null=False)
    direction = models.ForeignKey(Direction, verbose_name="Откуда/Куда", on_delete=models.CASCADE, null=False)
    location = models.ForeignKey(Location, verbose_name="Перемещение (место)", on_delete=models.CASCADE, null=False)
    quality = models.ForeignKey(AssortmentQualityCategory, verbose_name="Качество продукции", on_delete=models.CASCADE, null=False)
    quantity = models.DecimalField(max_digits=9, decimal_places=0, verbose_name="Количество", null=False)
    reason = models.TextField(max_length=2000, verbose_name="Причина перемещения", null=False)
    slug = AutoSlugField(populate_from='name', editable=False, always_update=True)
    date = models.DateField(verbose_name="Дата", auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/stock/{self.slug}'


class Test(models.Model):

    title = models.CharField(max_length=500)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User


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
    def func(**self):
        id_all = Product.objects.all()
        if not id_all:
            return 'SP00001'
        else:
            last = str(max(Product.objects.values_list('id'))[0] + 1)
            while len(last) < 5:
                last = str(0) + last
            last_number = str('SP') + last
        return last_number

    category = models.ForeignKey(AssortmentCategory, verbose_name="Категория", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, verbose_name="Название", null=False)
    description = models.TextField(max_length=2000, verbose_name="Описание", null=True, blank=True)
    slug = AutoSlugField(populate_from='number', editable=True, always_update=True)
    image = models.ImageField(verbose_name="Фотография", upload_to='photos_parts', default='default.jpg')
    comment = models.TextField(max_length=2000, verbose_name="Описание", null=True, blank=True)
    number = models.CharField(max_length=7, unique=True, default=func, verbose_name='Номер продукта')

    def __str__(self):
        return self.number

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

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'


class Transaction(models.Model):
    number = models.ForeignKey(Product, verbose_name="Номер продукта", on_delete=models.CASCADE, null=False)
    status = models.ForeignKey(Status, verbose_name="Статус", on_delete=models.CASCADE, null=False)
    direction = models.ForeignKey(Direction, verbose_name="Откуда/Куда", on_delete=models.CASCADE, null=False)
    location = models.ForeignKey(Location, verbose_name="Перемещение (место)", on_delete=models.CASCADE, null=False)
    quality = models.ForeignKey(AssortmentQualityCategory, verbose_name="Качество продукции", on_delete=models.CASCADE,
                                null=False)
    quantity = models.DecimalField(max_digits=9, decimal_places=0, verbose_name="Количество", null=False)
    reason = models.TextField(max_length=2000, verbose_name="Причина перемещения", null=False)
    slug = AutoSlugField(populate_from='number', editable=False, always_update=True)
    date = models.DateField(verbose_name="Дата", auto_now_add=True)
    author = models.ForeignKey(User,  on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.number

    def get_absolute_url(self):
        return f'/stock/{self.slug}'

# Generated by Django 4.1.6 on 2023-02-16 13:47

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion
import mainapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssortmentCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя категории')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=True, populate_from='name')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='AssortmentQualityCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя категории по качеству продукции')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=True, populate_from='name')),
            ],
            options={
                'verbose_name': 'Quality of category',
                'verbose_name_plural': 'Quality of categories',
            },
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Куда/Откуда')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Локация')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=True, populate_from='name')),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Описание')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=True, populate_from='number')),
                ('image', models.ImageField(default='default.jpg', upload_to='photos_parts', verbose_name='Фотография')),
                ('comment', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Описание')),
                ('number', models.CharField(default=mainapp.models.Product.func, max_length=7, unique=True, verbose_name='Номер продукта')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.assortmentcategory', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Product',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Куда/Откуда')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=0, max_digits=9, verbose_name='Количество')),
                ('reason', models.TextField(max_length=2000, verbose_name='Причина перемещения')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='number')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Дата')),
                ('direction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.direction', verbose_name='Откуда/Куда')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.location', verbose_name='Перемещение (место)')),
                ('number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.product', verbose_name='Номер продукта')),
                ('quality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.assortmentqualitycategory', verbose_name='Качество продукции')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.status', verbose_name='Статус')),
            ],
        ),
    ]

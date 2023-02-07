# Generated by Django 4.1.5 on 2023-01-29 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_alter_transaction_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=255, verbose_name='Статус')),
                ('category', models.CharField(max_length=255, null=True, verbose_name='Категория')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Описание')),
                ('slug', models.CharField(max_length=255, verbose_name='Слаг')),
                ('image', models.ImageField(default='default.jpg', upload_to='photos_parts', verbose_name='Фотография')),
                ('comment', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Описание')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Дата')),
                ('number', models.CharField(max_length=7, verbose_name='Номер продукта')),
            ],
            options={
                'verbose_name': 'ProductLog',
                'verbose_name_plural': 'ProductLog',
            },
        ),
    ]
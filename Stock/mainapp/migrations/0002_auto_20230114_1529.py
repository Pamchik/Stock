# Generated by Django 3.0.8 on 2023-01-14 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='slug',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Status', verbose_name='Статус'),
        ),
    ]
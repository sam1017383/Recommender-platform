# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-08 17:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_calificable'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_extras',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Imagen_fuente', models.CharField(max_length=255)),
                ('Calificacion_promedio', models.FloatField()),
                ('Precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Descuento', models.DecimalField(decimal_places=2, max_digits=3)),
                ('Fecha_alta', models.DateField(auto_now_add=True)),
                ('Product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
            options={
                'db_table': 'product_extras',
            },
        ),
    ]

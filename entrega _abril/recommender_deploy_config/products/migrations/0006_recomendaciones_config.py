# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-12 18:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_extras_fecha_calculo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recomendaciones_config',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=255)),
                ('algoritmo', models.CharField(max_length=255)),
                ('long_max', models.IntegerField()),
                ('parametro', models.IntegerField()),
            ],
            options={
                'db_table': 'recomendaciones_config',
            },
        ),
    ]

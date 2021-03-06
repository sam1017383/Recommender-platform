# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-12 18:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_delete_listas_recomendadores_config'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listas_recomendadores_config',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titulo_interfaz', models.CharField(max_length=255)),
                ('algoritmo_recomendador', models.CharField(max_length=100)),
                ('longitud_max', models.IntegerField()),
                ('param', models.FloatField()),
            ],
            options={
                'db_table': 'listas_recomendadores_config',
            },
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-13 19:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_listas_recomendadores_config'),
    ]

    operations = [
        migrations.AddField(
            model_name='listas_recomendadores_config',
            name='secuencia',
            field=models.IntegerField(default=0),
        ),
    ]

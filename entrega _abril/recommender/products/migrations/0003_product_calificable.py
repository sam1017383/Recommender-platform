# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-11 18:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20160208_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Calificable',
            field=models.BooleanField(default=1),
        ),
    ]
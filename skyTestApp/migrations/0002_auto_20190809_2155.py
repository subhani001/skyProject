# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-08-09 21:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skyTestApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='duration',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='net_duration',
            field=models.CharField(max_length=30),
        ),
    ]

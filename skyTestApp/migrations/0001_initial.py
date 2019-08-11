# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-08-09 21:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('status', models.CharField(max_length=30)),
                ('start_date', models.CharField(max_length=30)),
                ('end_date', models.CharField(max_length=30)),
                ('parent', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('net_duration', models.IntegerField()),
            ],
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-05 19:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20171005_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='date_registered',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='station',
            name='date_registered',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

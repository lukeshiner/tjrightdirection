# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 15:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hitcounter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hitcounter',
            name='trip',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]

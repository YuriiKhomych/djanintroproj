# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-20 14:23
from __future__ import unicode_literals

from django.db import migrations, models
import utils


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=13, null=True, validators=[utils.validate_phone]),
        ),
    ]
